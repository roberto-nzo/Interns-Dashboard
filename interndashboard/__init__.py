from flask import Flask, session
from .extensions import *
from .models import *


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'APSIOHF0EIFNO9GUOB'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///interndashboard.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

    db.init_app(app)

    admin = Admin(app, name='Admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Dashboard, db.session))
    admin.add_view(ModelView(Topic_create, db.session))
    admin.add_view(ModelView(appr_disappr, db.session))

    from interndashboard.main.routes import main
    from interndashboard.admin.routes import adminbp
    from interndashboard.users.routes import users
    from interndashboard.users.utils import utils

    app.register_blueprint(main)
    app.register_blueprint(adminbp)
    app.register_blueprint(users)
    app.register_blueprint(utils)

    return app
