import os
import unittest
from flask import current_app
from flask_testing import TestCase
from project import app


class TestDevelopmentConfig(TestCase):
    print("testing dev-env------", flush=True)

    def create_app(self):
        app.config.from_object('project.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        print("testing dev-env-is-development------", flush=True)
        self.assertTrue(app.config['SECRET_KEY'] == 'thisissecretandsecure')
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_URL')
        )


class TestTestingConfig(TestCase):
    print("testing test-env------", flush=True)

    def create_app(self):
        app.config.from_object('project.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        print("testing dev-env-is-testing ------", flush=True)
        self.assertTrue(app.config['SECRET_KEY'] == 'thisissecretandsecure')
        self.assertTrue(app.config['TESTING'])
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] ==
            os.environ.get('DATABASE_TEST_URL')
        )



if __name__ == '__main__':
    unittest.main()
