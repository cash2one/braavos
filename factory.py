from flask import Flask
from libs.db import db


def create_app(config_object='config.DevelopmentConfig'):
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(config_object)
    app.debug = app.config['DEBUG']
    db.init_app(app)
    db.app = app
    return app
