from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy

class SQLAlchemy(_BaseSQLAlchemy):
  def apply_pool_defaults(self, app, options):
    super(SQLAlchemy, self).apply_pool_defaults(app, options)
    options["pool_pre_ping"] = True

db = SQLAlchemy()