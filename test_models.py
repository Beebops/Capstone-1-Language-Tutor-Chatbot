import unittest
from app import app
from models import User, Chat, Message, db, connect_db


# Create a test case for your models by inheriting from unittest.TestCase
class ModelTests(unittest.TestCase):
    def setUp(self):
        # Set up the test database and other configurations
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "postgresql:///capstone_language_tutor_test"
        app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SECRET_KEY"] = "test-secret-key"
        connect_db(app)
        db.create_all()

    def tearDown(self):
        # Clean up the test database
        db.session.remove()
        db.drop_all()

    def test_create_chat(self):
        # Test creating a new chat
        user = User(
            username="testuser", email="test@example.com", password="testpassword"
        )
        db.session.add(user)
        db.session.commit()

        chat = Chat.create_chat(user.id, "spanish", "b1")

        self.assertIsNotNone(chat.id)
        self.assertEqual(chat.user_id, user.id)
        self.assertEqual(chat.language, "spanish")
        self.assertEqual(chat.language_level, "b1")


if __name__ == "__main__":
    unittest.main()
