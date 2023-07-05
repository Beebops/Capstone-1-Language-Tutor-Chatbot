import unittest
from flask_testing import TestCase
from app import app
from models import db, connect_db


# Create a test Flask app by inheriting from TestCase
class ViewIntegrationTests(TestCase):
    def create_app(self):
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "postgresql:///capstone_language_tutor_test"
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["WTF_CSRF_ENABLED"] = False
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SECRET_KEY"] = "test-secret-key"
        connect_db(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # Define your integration tests as methods starting with 'test_'
    def test_index_page(self):
        # Test the index route '/'
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        # Add more assertions to validate the response

    def test_new_chat_page(self):
        # Test the '/home' route for creating a new chat
        with self.client:
            # Log in a user before accessing the protected route
            self.client.post(
                "/login", data={"username": "testuser", "password": "testpassword"}
            )
            response = self.client.get("/home")
            self.assertEqual(response.status_code, 200)
            # Add more assertions to validate the response

    # Add more tests for other views


if __name__ == "__main__":
    unittest.main()
