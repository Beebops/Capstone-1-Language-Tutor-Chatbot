import unittest
from flask_testing import TestCase
from app import app
from models import db, User, Message, Chat, bcrypt
from forms import new_chat_form, title_chat_form
from flask import url_for

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone_language_tutor_test"
app.config["SQLALCHEMY_ECHO"] = False
app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class TestUserViews(TestCase):
    def create_app(self):
        return app

    def setUp(self):
        """Add a sample User"""

        User.query.delete()

        user = User.signup("testuser1", "test1@example.com", "testpassword")
        self.user_id = user.id
        self.user_username = user.username
        self.user = user

        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.rollback()

    def test_display_chats_route(self):
        """Test the display_chats route"""

        with app.test_client() as client:
            # Login the user
            client.post(
                "/login",
                data={"username": self.user.username, "password": "testpassword"},
                follow_redirects=True,
            )

            # Access the /chats/<user_id> route
            response = client.get(f"/chats/{self.user.id}")

            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Your Chats", response.data)

    def test_new_chat_route(self):
        """Test the new_chat route"""

        with app.test_client() as client:
            # Login the user
            client.post(
                "/login",
                data={"username": self.user.username, "password": "testpassword"},
                follow_redirects=True,
            )

            # Create a new chat
            response = client.post(
                "/home",
                data={"language": "spanish", "language_level": "b1"},
                follow_redirects=True,
            )

            self.assert200(response)
            self.assertIn(b"New Chat", response.data)
            self.assertEqual(len(Chat.query.all()), 1)
            chat = Chat.query.first()
            self.assertEqual(chat.user_id, self.user.id)
            self.assertEqual(chat.language, "spanish")
            self.assertEqual(chat.language_level, "b1")


if __name__ == "__main__":
    unittest.main()
