import unittest
from flask_sqlalchemy import SQLAlchemy
from weather_app import create_app, db
from weather_app.models import City
from config import Config
import os

# db = SQLAlchemy()

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'

class BasicTestCase(unittest.TestCase):

    def setUp(self):

        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # self.db = SQLAlchemy()
        # self.app_context = self.app.app_context()
        # self.app_context.push() # check

    def test_main_page(self):
        """ensure that mainpage type is html/txt and it is accessible"""
        response = self.app.get('/', content_type='html/txt')
        self.assertEqual(response.status_code, 201)

    def tearDown(self):
        pass
        # db.session.remove()
        # db.drop_all()
        # os.remove("./test.db")

