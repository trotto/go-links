import logging
import re
import string
from urllib.parse import urlparse, urlencode, urlunparse

import validators
from validators.utils import ValidationFailure

from modules.data import get_models
from modules.organizations.utils import get_organization_id_for_email
from shared_helpers import config
from shared_helpers.encoding import convert_entity_to_dict
from shared_helpers.events import enqueue_event
from shared_helpers.utils import get_from_key_path


models = get_models('links')


class LinkCreationException(Exception):
  pass


def _matches_pattern(keywords_punctuation_sensitive, provided_shortpath, candidate_match):
  provided_shortpath_components = provided_shortpath.split('/')
  candidate_match_components = candidate_match.split('/')

  if len(provided_shortpath_components) != len(candidate_match_components):
    return None

  matching_formatting_args = []

  for i in range(len(provided_shortpath_components)):
    if candidate_match_components[i] == '%s':
      matching_formatting_args.append(provided_shortpath_components[i])
    elif candidate_match_components[i] != get_canonical_keyword(keywords_punctuation_sensitive, provided_shortpath_components[i]):
      return None

  return matching_formatting_args or None


def derive_pattern_match(organization, keywords_punctuation_sensitive, namespace, shortpath):
  if '/' not in shortpath:  # paths without a second part can't be pattern-matching
    return None, None

  prefix_matches = models.ShortLink.get_by_prefix(organization, namespace, shortpath.split('/')[0])

  matching_shortlink = None
  matching_formatting_args = None
  for prefix_match in prefix_matches:
    if '%s' not in prefix_match.shortpath:
      continue

    matching_formatting_args = _matches_pattern(keywords_punctuation_sensitive, shortpath, prefix_match.shortpath)
    if not matching_formatting_args:
      continue
    else:
      matching_shortlink = prefix_match
      break

  if not matching_shortlink:
    return None, None

  return matching_shortlink, matching_shortlink.destination_url.replace(
    '%', '%%').replace('%%s', '%s') % tuple(matching_formatting_args)


def _percent_encode_if_not_ascii_compatible(unicode_char):
  try:
    return unicode_char.encode('ascii').decode('ascii')
  except UnicodeEncodeError:
    return urlencode({'': unicode_char.encode('utf8')})[1:]


def _encode_ascii_incompatible_chars(destination):
  return ''.join(_percent_encode_if_not_ascii_compatible(ch) for ch in destination)


def get_shortlink(organization, keywords_punctuation_sensitive, alternative_resolution_mode, namespace, keyword):
  """Returns (shortlink_object, actual_destination)."""
  canonical_keyword = get_canonical_keyword(keywords_punctuation_sensitive, keyword)
  perfect_match = models.ShortLink.get_by_full_path(organization, namespace, canonical_keyword)

  if perfect_match:
    return perfect_match, perfect_match.destination_url

  matching_programmatic_link, destination = derive_pattern_match(organization, keywords_punctuation_sensitive, namespace, keyword)
  if matching_programmatic_link:
    return matching_programmatic_link, destination

  if alternative_resolution_mode:
    keyword_parts = canonical_keyword.split('/')
    if len(keyword_parts) > 1:
      perfect_prefix_match = models.ShortLink.get_by_full_path(organization, namespace, keyword_parts[0])

      if perfect_prefix_match:
        return perfect_prefix_match, perfect_prefix_match.destination_url+'/'.join(keyword_parts[1:])
    else:
      # search for prefix match and, if found, resolve with empty string for placeholders
      prefix_matches = models.ShortLink.get_by_prefix(organization, namespace, keyword_parts[0])

      if len(prefix_matches) > 1:
        logging.error('Multiple prefix matches for keyword %s in org %s, which is using alternative resolution mode', organization, keyword)
        # fall through to the first match

      if len(prefix_matches) > 0:
        return prefix_matches[0], prefix_matches[0].destination_url.replace('%s', '')

  return None, None


def find_conflicting_link(organization, namespace, shortpath):
  if '%s' not in shortpath:
    raise ValueError('Provided shortpath must be a programmatic link containing "%s"')

  shortpath_parts = shortpath.split('/')
  shortpath_prefix = shortpath_parts[0]

  links_with_prefix = models.ShortLink.get_by_prefix(organization,
                                                     namespace,
                                                     shortpath_prefix)

  for link in links_with_prefix:
    other_shortpath_parts = link.shortpath.split('/')
    if len(shortpath_parts) != len(other_shortpath_parts):
      continue
    
    found_conflicting_part = False
    for i in range(0, len(shortpath_parts)):
      if shortpath_parts[i] != '%s' and shortpath_parts[i] != other_shortpath_parts[i]:
        found_conflicting_part = True
        break

    if not found_conflicting_part:
      return link

  return None


def create_short_link(acting_user, organization, owner, namespace, shortpath, destination, validation_mode):
  return upsert_short_link(acting_user, organization, owner, namespace, shortpath, destination, None, validation_mode)


def update_short_link(acting_user, link_object):
  return upsert_short_link(acting_user,
                           link_object.organization, link_object.owner, link_object.namespace, link_object.shortpath,
                           link_object.destination_url, link_object)


def check_namespaces(organization, namespace, shortpath):
  org_namespaces = config.get_organization_config(organization).get('namespaces', [])
  default_namespace = config.get_default_namespace(organization)

  if namespace != default_namespace and namespace not in org_namespaces:
    raise LinkCreationException('"%s" is not a valid link prefix for your organization' % (namespace))

  # If an organization has a namespace of, for example, "eng", go/eng can be created, but go/eng/%s would conflict
  # with eng/something, as {base}/eng/something is how users without an extension installed can still easily
  # access links in the "eng" namespace.
  if namespace == default_namespace:
    shortpath_parts = shortpath.split('/')
    if len(shortpath_parts) > 1 and shortpath_parts[0] in org_namespaces:
      raise LinkCreationException('"%s" is a reserved prefix for your organization' % (shortpath_parts[0]))


SIMPLE_VALIDATION_MODE = 'simple'
EXPANDED_VALIDATION_MODE = 'expanded'
PATH_RESTRICTIONS_ERROR_SIMPLE = 'Keywords can include only letters, numbers, hyphens, "/", and "%s" placeholders'
PATH_RESTRICTIONS_ERROR_EXPANDED = 'Provided keyword is invalid' # TODO: Include invalid char(s) in error
KEYWORDS_PUNCTUATION_SENSITIVE_DEFAULT = True
ALTERNATIVE_KEYWORD_RESOLUTION_MODE = 'alternative'
DEFAULT_VALIDATION_REGEX = '[^0-9a-zA-Z\-\/%]'


def get_keyword_validation_regex(org_settings):
  return get_from_key_path(org_settings or {}, ['keywords', 'validation_regex']) or DEFAULT_VALIDATION_REGEX


def validate_shortpath(organization, shortpath, validation_mode):
  validation_regex = get_keyword_validation_regex(config.get_organization_config(organization))

  if validation_mode == SIMPLE_VALIDATION_MODE:
    if shortpath != re.sub(validation_regex, '', shortpath):
      raise LinkCreationException(PATH_RESTRICTIONS_ERROR_SIMPLE)
  elif validation_mode == EXPANDED_VALIDATION_MODE:
    if type(validators.url('https://trot.to/'+shortpath)) is ValidationFailure:
      raise LinkCreationException(PATH_RESTRICTIONS_ERROR_EXPANDED)
  else:
    raise ValueError(f'Unsupported validation mode {validation_mode}')


"""Returns whether or not the provided destination is a valid URL using a bare hostname, like `http://go/directory`.

This function is used to work around a limitation of the `validators` package where it doesn't recognize URLs using
bare hostnames as valid. 
"""
def _is_valid_bare_hostname_destination(destination):
  url_parts = urlparse(destination)

  if not url_parts.netloc or '.' in url_parts.netloc:
    return False

  netloc_parts = url_parts.netloc.split(':', 1)
  netloc_parts[0] = netloc_parts[0] + '.com'

  url_parts = url_parts._replace(netloc=':'.join(netloc_parts))

  with_tld = urlunparse(url_parts)

  return type(validators.url(with_tld)) is not ValidationFailure

"""Returns whether or not the provided destination is a valid URL using double hyphen, like `https://double--hyphen.example.com/some/path`.

This function is used to work around a limitation of the `validators` package where it doesn't recognize URLs with double hypens valid
"""
def _is_valid_idn_destination(destination):
  clean_url = re.sub('\-\-+', '-', destination)

  return type(validators.url(clean_url)) is not ValidationFailure

def _validate_destination(destination):
  if type(validators.url(destination)) is ValidationFailure and not _is_valid_bare_hostname_destination(destination) and not _is_valid_idn_destination(destination):
    raise LinkCreationException('You must provide a valid destination URL')


PUNCTUATION_SCRUBBED = string.punctuation.replace('/', '').replace('%', '')


def _remove_punctuation(keyword):
  return keyword.translate(str.maketrans('', '', PUNCTUATION_SCRUBBED))


def are_keywords_punctuation_sensitive(org_config):
  keywords_punctuation_sensitive = config.get_from_key_path(org_config, ['keywords', 'punctuation_sensitive'])

  if keywords_punctuation_sensitive is None:
    return KEYWORDS_PUNCTUATION_SENSITIVE_DEFAULT

  return keywords_punctuation_sensitive


def is_using_alternative_keyword_resolution(org_config):
  return ALTERNATIVE_KEYWORD_RESOLUTION_MODE == config.get_from_key_path(org_config, ['keywords', 'resolution_mode'])


def get_canonical_keyword(punctuation_sensitive, keyword):
  return keyword if punctuation_sensitive else _remove_punctuation(keyword)


def upsert_short_link(acting_user, organization, owner, namespace, shortpath, destination, updated_link_object, validation_mode=EXPANDED_VALIDATION_MODE):
  shortpath = shortpath.strip().lower().strip('/')
  destination = destination.strip()

  if not shortpath:
    raise LinkCreationException('You must provide a path')

  validate_shortpath(organization, shortpath, validation_mode)

  display_shortpath = shortpath
  org_config = config.get_organization_config(organization)

  if org_config.get('read_only_mode') and not updated_link_object and validation_mode != EXPANDED_VALIDATION_MODE:
    raise LinkCreationException('Your organization is in read-only mode.')

  alternative_resolution_mode = is_using_alternative_keyword_resolution(org_config)
  keywords_punctuation_sensitive = are_keywords_punctuation_sensitive(org_config)
  shortpath = get_canonical_keyword(keywords_punctuation_sensitive, shortpath)

  check_namespaces(organization, namespace, shortpath)

  if acting_user and (not (organization == acting_user.organization and owner == acting_user.email)
      and organization != get_organization_id_for_email(owner)):
    raise LinkCreationException("The go link's owner must be in the go link's organization")

  shortpath_parts = shortpath.split('/')
  if len(shortpath_parts) > 1:
    if alternative_resolution_mode:
      if shortpath_parts[1] != '%s':
        raise LinkCreationException('Only "%s" placeholders are allowed after the first "/" in a keyword')

    placeholder_found = False

    for part in shortpath_parts[1:]:
      if part == '%s':
        placeholder_found = True
      elif placeholder_found:
        raise LinkCreationException('After the first "%s" placeholder, you can only have additional placeholders')

  if '%' in shortpath:
    if '%' in shortpath and shortpath.count('%') != shortpath.count('%s'):
      raise LinkCreationException(PATH_RESTRICTIONS_ERROR_SIMPLE)

    if '%s' in shortpath.split('/')[0]:
      raise LinkCreationException('"%s" placeholders must come after a "/". Example: "jira/%s"')

    if shortpath.count('%s') != destination.count('%s'):
      raise LinkCreationException('The keyword and the destination must have the same number of "%s" placeholders')

  if not updated_link_object:
    existing_link, _ = get_shortlink(organization, keywords_punctuation_sensitive, alternative_resolution_mode, namespace, shortpath)

    if existing_link:
      error_message = 'That go link already exists. %s/%s points to %s' % (namespace,
                                                                           existing_link.display_shortpath or existing_link.shortpath,
                                                                           existing_link.destination_url)

      if existing_link.shortpath != shortpath:
        error_message = 'A conflicting go link already exists. %s/%s points to %s' % (namespace,
                                                                                      existing_link.shortpath,
                                                                                      existing_link.destination_url)

      raise LinkCreationException(error_message)

    if '%s' in shortpath:
      conflicting_link = find_conflicting_link(organization, namespace, shortpath)

      if conflicting_link:
        raise LinkCreationException('A conflicting go link already exists. %s/%s points to %s'
                                    % (namespace, conflicting_link.shortpath, conflicting_link.destination_url))

  # Note: urlparse('128.90.0.1:8080/start').scheme returns '128.90.0.1'. Hence the additional checking.
  destination_url_scheme = urlparse(destination).scheme
  if (not destination_url_scheme
      or not destination_url_scheme.strip()
      or not destination.startswith(destination_url_scheme + '://')):
    # default to HTTP (see Slack discussion)
    destination = 'http://' + destination

  _validate_destination(destination)

  if updated_link_object:
    link = updated_link_object
  else:
    link_kwargs = {'organization': organization,
                   'owner': owner,
                   'namespace': namespace,
                   'display_shortpath': display_shortpath,
                   'shortpath': shortpath,
                   'destination_url': destination,
                   'shortpath_prefix': shortpath.split('/')[0]}
    link = models.ShortLink(**link_kwargs)

  link.put()

  link_dict = convert_entity_to_dict(link, ['owner', 'shortpath', 'destination_url', 'organization'])
  link_dict['id'] = link.get_id()

  enqueue_event(link.organization,
                'link.%s' % ('updated' if updated_link_object else 'created'),
                'link',
                link_dict)

  return link


def get_all_shortlinks_for_org(user_organization):
  shortlinks = []

  for shortlink in models.ShortLink.get_by_organization(user_organization):
    shortlinks.append(shortlink)

  return shortlinks
