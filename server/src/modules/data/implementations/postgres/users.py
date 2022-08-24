import datetime

from sqlalchemy.dialects.postgresql import JSON

from main import db
from modules.data.abstract import users


class User(db.Model, users.User):

  id = db.Column(db.Integer, primary_key=True)
  created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)
  email = db.Column(db.String(120),
                    index=True,
                    unique=True,
                    nullable=False)
  organization = db.Column(db.String(80),
                           nullable=False)
  enabled = db.Column(db.Boolean, default=True)
  role = db.Column(db.String(30))
  accepted_terms_at = db.Column(db.DateTime)
  domain_type = db.Column(db.String(30))
  notifications = db.Column(JSON)

  @staticmethod
  def get_by_id(id):
    return User.query.get(int(id))

  @staticmethod
  def get_by_email_and_org(email, org):
    return User.query.filter(User.email == email, User.organization == org).one_or_none()

  def put(self):
    super().put()

    db.session.add(self)
    db.session.commit()
