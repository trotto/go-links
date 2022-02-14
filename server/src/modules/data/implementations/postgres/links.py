import base64
import datetime

from main import db
from modules.data.abstract import links
from shared_helpers.config import get_default_namespace


def _get_link_key(organization, namespace, shortpath):
  # go/17

  ns_and_path = (shortpath
                 if namespace == get_default_namespace(organization) or not namespace
                 else f'{namespace}:{shortpath}')

  # keys were misformatted like `b'Z29vZ3MuY29t':roadmap` originally, and now this misformatting is
  # done explicitly rather than updating all existing rows
  return f"b'{base64.b64encode(bytes(organization, 'utf-8')).decode('utf-8')}':{ns_and_path}"


def set_namespace_prop(link):
  link.namespace = link._ns or get_default_namespace(link.organization)

  return link


class ShortLink(db.Model, links.ShortLink):

  id = db.Column(db.Integer, primary_key=True)
  key = db.Column(db.String(500),
                  index=True,
                  unique=True,
                  nullable=False)
  created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  organization = db.Column(db.String(80),
                           nullable=False)
  owner = db.Column(db.String(120),
                    nullable=False)
  _ns = db.Column('namespace',
                  db.String(30),
                  nullable=True)
  display_shortpath = db.Column(db.String(200),
                                index=True,
                                nullable=True)
  shortpath = db.Column(db.String(200),
                        index=True,
                        nullable=False)
  shortpath_prefix = db.Column(db.String(200),
                               index=True,
                               nullable=False)
  destination_url = db.Column(db.String(3000),
                              nullable=False)
  type = db.Column(db.String(30))
  visits_count = db.Column(db.Integer)
  visits_count_last_updated = db.Column(db.DateTime)

  # the namespace property is used to abstract away the fact the default namespace ("go" by default) is stored as null
  # in the database
  namespace = None

  @staticmethod
  def get_by_id(id):
    link = ShortLink.query.get(int(id))

    return set_namespace_prop(link) if link else None

  @staticmethod
  def get_by_prefix(organization, namespace, shortpath_prefix):
    links = ShortLink.query \
        .filter(ShortLink.organization == organization) \
        .filter(ShortLink._ns == (namespace if namespace != get_default_namespace(organization) else None)) \
        .filter(ShortLink.shortpath_prefix == shortpath_prefix) \
        .all()

    return [set_namespace_prop(l) for l in links]

  @staticmethod
  def get_by_full_path(organization, namespace, shortpath):
    link = ShortLink.query \
        .filter(ShortLink.key == _get_link_key(organization, namespace, shortpath)) \
        .one_or_none()

    return set_namespace_prop(link) if link else None

  @staticmethod
  def get_by_organization(organization):
    links = ShortLink.query \
        .filter(ShortLink.organization == organization) \
        .all()

    return [set_namespace_prop(l) for l in links]

  def put(self):
    super().put()

    self.key = _get_link_key(self.organization, self.namespace, self.shortpath)

    self._ns = self.namespace if self.namespace != get_default_namespace(self.organization) else None

    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def _get_all():
    return ShortLink.query.all()


db.Index('org_ns_prefix', ShortLink.organization, ShortLink._ns, ShortLink.shortpath_prefix)
