from flask import Flask
from .extensions import db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'APSIOHF0EIFNO9GUOB'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interndashboard.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from interndashboard.main.routes import main
    from interndashboard.admin.routes import admin
    from interndashboard.users.routes import users
    from interndashboard.users.utils import utils

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(users)
    app.register_blueprint(utils)

    return app