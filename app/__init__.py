from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5

from .config import Config

db = SQLAlchemy()
bootstrap = Bootstrap5()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bootstrap.init_app(app)

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
