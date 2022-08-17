from flask import Flask
from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def create_app(config_class=Config):
    app = Flask(__name__)

    app.config.from_object(Config)
    mysql.init_app(app)

    from interndashboard.main.routes import main
    from interndashboard.admin.routes import admin
    from interndashboard.users.routes import users
    from interndashboard.users.utils import utils

    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(users)
    app.register_blueprint(utils)

    return app