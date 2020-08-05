import datetime

from main import db
from modules.data.abstract import links


class ShortLink(db.Model, links.ShortLink):

  id = db.Column(db.Integer, primary_key=True)
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
        .filter(ShortLink.shortpath == shortpath) \
        .filter(ShortLink.organization == organization) \
        .one_or_none()

  @staticmethod
  def get_by_organization(organization):
    return ShortLink.query \
        .filter(ShortLink.organization == organization) \
        .all()

  def put(self):
    super().put()

    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()
