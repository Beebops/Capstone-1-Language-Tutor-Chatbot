import unittest
from unittest import TestCase, mock
from app import app
from datetime import datetime
from models import User, Chat, Message, db, bcrypt

app.config["TESTING"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///capstone_language_tutor_test"
app.config["SQLALCHEMY_ECHO"] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    def setUp(self):
        """Clean up existing Users"""
        User.query.delete()

    def tearDown(self):
        """Clean up fouled transactions"""
        db.session.rollback()

    def test_signup(self):
        """Test user signup"""
        user = User.signup("testuser1", "test1@example.com", "testpassword")
        db.session.commit()

        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "testuser1")
        self.assertEqual(user.email, "test1@example.com")
        self.assertTrue(bcrypt.check_password_hash(user.password, "testpassword"))

    def test_authenticate_valid_credentials(self):
        """Test user authentication with valid credentials"""
        user = User.signup("testuser2", "test2@example.com", "testpassword2")
        db.session.commit()

        # Mock the login_user function
        with mock.patch("models.login_user") as mock_login_user:
            authenticated_user = User.authenticate("testuser2", "testpassword2")

            self.assertEqual(authenticated_user, user)
            mock_login_user.assert_called_with(
                user
            )  # Verify that login_user was called

    def test_authenticate_invalid_credentials(self):
        """Test user authentication with invalid credentials"""
        user = User.signup("testuser3", "test3@example.com", "testpassword3")
        db.session.commit()

        authenticated_user = User.authenticate("testuser3", "wrongpassword")

        self.assertFalse(authenticated_user)

    def test_authenticate_nonexistent_user(self):
        """Test user authentication with a nonexistent user"""
        authenticated_user = User.authenticate("nonexistentuser", "testpassword")

        self.assertFalse(authenticated_user)


class MessageModelTestCase(TestCase):
    def setUp(self):
        """Clean up existing Messages"""
        Message.query.delete()
        Chat.query.delete()

    def tearDown(self):
        """Clean up fouled transactions"""
        db.session.rollback()

    def test_create_message(self):
        """Test creating a new message"""
        user = User(
            username="testuser4", email="test4@example.com", password="testpassword"
        )
        db.session.add(user)
        db.session.commit()

        chat = Chat.create_chat(user.id, "spanish", "b1")

        timestamp = datetime.utcnow()
        message = Message.create_message(chat.id, "user", "Hello", timestamp)

        self.assertIsNotNone(message.id)
        self.assertEqual(message.chat_id, chat.id)
        self.assertEqual(message.role, "user")
        self.assertEqual(message.content, "Hello")
        self.assertEqual(message.timestamp, timestamp)

    def test_get_messages_by_chat(self):
        """Test retrieving messages by chat id"""
        user = User(
            username="testuser5", email="test5@example.com", password="testpassword"
        )
        db.session.add(user)
        db.session.commit()

        chat = Chat.create_chat(user.id, "spanish", "b1")

        message1 = Message.create_message(chat.id, "user", "Hello", datetime.utcnow())
        message2 = Message.create_message(chat.id, "assistant", "Hi", datetime.utcnow())

        messages = Message.get_messages_by_chat(chat.id)

        self.assertEqual(len(messages), 2)
        self.assertEqual(
            messages[0], message1
        )  # Messages should be ordered by timestamp, with the latest first
        self.assertEqual(messages[1], message2)


class ChatModelTestCase(TestCase):
    def setUp(self):
        """Clean up existing Chats"""
        Chat.query.delete()

    def tearDown(self):
        """Clean up fouled transactions"""

        db.session.rollback()

    def test_create_chat(self):
        """Test creating a new chat"""
        user = User(
            username="testuser6", email="test6@example.com", password="testpassword"
        )
        db.session.add(user)
        db.session.commit()

        chat = Chat.create_chat(user.id, "spanish", "b1")

        self.assertIsNotNone(chat.id)
        self.assertEqual(chat.user_id, user.id)
        self.assertEqual(chat.language, "spanish")
        self.assertEqual(chat.language_level, "b1")

    def test_get_chats_by_user(self):
        """Test retrieving chats of given user id"""
        user = User(
            username="testuser7", email="test7@example.com", password="testpassword"
        )
        db.session.add(user)
        db.session.commit()

        chat1 = Chat.create_chat(user.id, "spanish", "b1")
        chat2 = Chat.create_chat(user.id, "french", "a2")

        chats = Chat.get_chats_by_user(user.id).all()

        self.assertEqual(len(chats), 2)
        self.assertEqual(chats[0], chat2)
        self.assertEqual(chats[1], chat1)

    def test_get_chat_title(self):
        """Test retrieving the title of a chat"""
        chat = Chat.create_chat(1, "spanish", "c1")
        chat.chat_title = "La Tienda"
        db.session.commit()

        title = Chat.get_chat_title(chat.id)

        self.assertEqual(title, "La Tienda")

    def test_get_chat_title_nonexistent_chat(self):
        """Test retrieving the title of a nonexistent chat"""
        title = Chat.get_chat_title(9999)

        self.assertEqual(title, "Untitled Chat")

    def test_delete_chat(self):
        """Test deleting a chat"""
        user = User(
            username="testuser8", email="test8@example.com", password="testpassword"
        )
        db.session.add(user)
        db.session.commit()

        chat = Chat.create_chat(user.id, "spanish", "b1")

        self.assertIsNotNone(Chat.query.get(chat.id))

        chat.delete_chat()

        self.assertIsNone(Chat.query.get(chat.id))


if __name__ == "__main__":
    unittest.main()
