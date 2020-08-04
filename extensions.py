from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_bootstrap import Bootstrap
from flask_login import LoginManager


db = SQLAlchemy()

migrate = Migrate(db)


bootstrap = Bootstrap()


login_manager = LoginManager()
