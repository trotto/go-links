import base64
import datetime

from main import db
from modules.data.abstract import links


def _get_link_key(organization, shortpath):
  # go/17
  return f'{base64.b64encode(bytes(organization, "utf-8"))}:{shortpath}'


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
  shortpath = db.Column(db.String(200),
                        index=True,
                        nullable=False)
  shortpath_prefix = db.Column(db.String(200),
                               index=True,
                               nullable=False)
  destination_url = db.Column(db.String(3000),
                              nullable=False)
  visits_count = db.Column(db.Integer)
  visits_count_last_updated = db.Column(db.DateTime)

  @staticmethod
  def get_by_id(id):
    return ShortLink.query.get(int(id))

  @staticmethod
  def get_by_prefix(organization, shortpath_prefix):
    return ShortLink.query \
        .filter(ShortLink.shortpath_prefix == shortpath_prefix) \
        .filter(ShortLink.organization == organization) \
        .all()

  @staticmethod
  def get_by_full_path(organization, shortpath):
    return ShortLink.query \
        .filter(ShortLink.key == _get_link_key(organization, shortpath)) \
        .one_or_none()

  @staticmethod
  def get_by_organization(organization):
    return ShortLink.query \
        .filter(ShortLink.organization == organization) \
        .all()

  def put(self):
    super().put()

    self.key = _get_link_key(self.organization, self.shortpath)

    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  @staticmethod
  def _get_all():
    return ShortLink.query.all()
