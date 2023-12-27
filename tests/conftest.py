import pytest
import os
from dotenv import load_dotenv

from app import create_app


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True


@pytest.fixture()
def app():
    app = create_app(config_class=Config)
    return app


@pytest.fixture()
def client(app):
    return app.test_client()
