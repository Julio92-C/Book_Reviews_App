from flask import Flask, Blueprint
from extensions import db, login_manager, migrate
import extensions
from views import main


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'Thisismysecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:921016@localhost/books'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    extensions.bootstrap.init_app(app)

    extensions.migrate.init_app(app)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    app.register_blueprint(main)

    return app


if __name__ == '__main__':
    manager.run()
