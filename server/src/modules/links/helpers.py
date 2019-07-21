import datetime
import re
import urllib
import urlparse

import validators
from validators.utils import ValidationFailure

import models
from modules.users.helpers import get_or_create_user
from shared_helpers.encoding import convert_entity_to_dict
from shared_helpers.events import enqueue_event


class LinkCreationException(Exception):
  pass


def _matches_pattern(provided_shortpath, candidate_match):
  provided_shortpath_components = provided_shortpath.split('/')
  candidate_match_components = candidate_match.split('/')

  if len(provided_shortpath_components) != len(candidate_match_components):
    return None

  matching_formatting_args = []

  for i in xrange(len(provided_shortpath_components)):
    if candidate_match_components[i] == '%s':
      matching_formatting_args.append(provided_shortpath_components[i])
    elif candidate_match_components[i] != provided_shortpath_components[i]:
      return None

  return matching_formatting_args or None


def derive_pattern_match(organization, shortpath):
  if '/' not in shortpath:  # paths without a second part can't be pattern-matching
    return None, None

  prefix_matches = models.ShortLink.query(
      models.ShortLink.organization == organization,
      models.ShortLink.shortpath_prefix == shortpath.split('/')[0]).fetch(limit=None)

  matching_shortlink = None
  matching_formatting_args = None
  for prefix_match in prefix_matches:
    if '%s' not in prefix_match.shortpath:
      continue

    matching_formatting_args = _matches_pattern(shortpath, prefix_match.shortpath)
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
    return unicode_char.encode('ascii')
  except UnicodeEncodeError:
    return urllib.urlencode({'': unicode_char.encode('utf8')})[1:]


def _encode_ascii_incompatible_chars(destination):
  return ''.join(_percent_encode_if_not_ascii_compatible(ch) for ch in destination)


def get_shortlink(organization, shortpath):
  """Returns (shortlink_object, actual_destination)."""
  perfect_match = models.ShortLink.query(
      models.ShortLink.organization == organization,
      models.ShortLink.shortpath == shortpath).get()

  if perfect_match:
    return perfect_match, perfect_match.destination_url

  if not perfect_match:
    return derive_pattern_match(organization, shortpath)


def create_short_link(organization, creator, shortpath, destination):
  return upsert_short_link(organization, creator, shortpath, destination, None)


def update_short_link(link_object):
  return upsert_short_link(link_object.organization, link_object.owner,
                           link_object.shortpath, link_object.destination_url,
                           link_object)


def upsert_short_link(organization, creator, shortpath, destination, updated_link_object):
  shortpath = shortpath.strip().lower().strip('/')
  destination = _encode_ascii_incompatible_chars(destination.strip())

  # TODO: Cache this.
  user = get_or_create_user(creator, organization)
  if not user.accepted_terms_at:
    user.accepted_terms_at = datetime.datetime.utcnow()
    user.put()

  if not shortpath:
    raise LinkCreationException('You must provide a path')

  PATH_RESTRICTIONS_ERROR = 'Keywords can include only letters, numbers, hyphens, "/", and "%s" placeholders'

  if shortpath != re.sub('[^0-9a-zA-Z\-\/%]', '', shortpath):
    raise LinkCreationException(PATH_RESTRICTIONS_ERROR)

  shortpath_parts = shortpath.split('/')
  if len(shortpath_parts) > 1:
    for part in shortpath_parts[1:]:
      if part != '%s':
        raise LinkCreationException('Keywords can have only "%s" placeholders after the first "/". Ex: "drive/%s"')

  if '%' in shortpath:
    if '%' in shortpath and shortpath.count('%') != shortpath.count('%s'):
      raise LinkCreationException(PATH_RESTRICTIONS_ERROR)

    if '%s' in shortpath.split('/')[0]:
      raise LinkCreationException('"%s" placeholders must come after a "/". Example: "jira/%s"')

    if shortpath.count('%s') != destination.count('%s'):
      raise LinkCreationException('The keyword and the destination must have the same number of "%s" placeholders')

  if not updated_link_object:
    existing_link, _ = get_shortlink(organization, shortpath)

    if existing_link:
      raise LinkCreationException('That go link already exists. go/%s points to %s'
                                  % (shortpath, existing_link.destination_url))

  # Note: urlparse.urlparse('128.90.0.1:8080/start').scheme returns '128.90.0.1'. Hence the additional checking.
  destination_url_scheme = urlparse.urlparse(destination).scheme
  if (not destination_url_scheme
      or not destination_url_scheme.strip()
      or not destination.startswith(destination_url_scheme + '://')):
    # default to HTTP (see Slack discussion)
    destination = 'http://' + destination

  if type(validators.url(destination)) is ValidationFailure:
    raise LinkCreationException('You must provide a valid destination URL')

  if updated_link_object:
    link = updated_link_object
  else:
    link_kwargs = {'organization': organization,
                   'owner': creator,
                   'shortpath': shortpath,
                   'destination_url': destination,
                   'shortpath_prefix': shortpath.split('/')[0]}
    link = models.ShortLink(**link_kwargs)

  link.put()

  link_dict = convert_entity_to_dict(link, ['owner', 'shortpath', 'destination_url', 'organization'])
  link_dict['id'] = link.key.id()

  enqueue_event('link.%s' % ('updated' if updated_link_object else 'created'),
                'link',
                link_dict)
  return link


def get_all_shortlinks_for_org(user_organization):
  shortlinks = []

  # TODO: Handle more links (paginate).
  for shortlink in models.ShortLink.query(models.ShortLink.organization == user_organization).fetch(limit=10000):
    shortlinks.append(shortlink)

  return shortlinks
