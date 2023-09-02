
from flask import Flask
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Message, Follows
from app import app

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Lukadon1996$@localhost/warbler'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  
        return app

    def setUp(self):
        self.app = self.create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.u1 = User.signup("user1", "user1@example.com", "password1", None)
        self.u2 = User.signup("user2", "user2@example.com", "password2", None)

        db.session.commit()

        self.u1 = User.query.filter_by(username='user1').first()
        self.u2 = User.query.filter_by(username='user2').first()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_model(self):
        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

    def test_user_follows(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertEqual(len(self.u2.following), 0)
        self.assertEqual(len(self.u2.followers), 1)
        self.assertEqual(len(self.u1.followers), 0)
        self.assertEqual(len(self.u1.following), 1)


    def test_is_following(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u1.is_following(self.u2))
        self.assertFalse(self.u2.is_following(self.u1))

    def test_is_followed_by(self):
        self.u1.following.append(self.u2)
        db.session.commit()

        self.assertTrue(self.u2.is_followed_by(self.u1))
        self.assertFalse(self.u1.is_followed_by(self.u2))

    def test_valid_signup(self):
        u_test = User.signup("testuser3", "testuser3@example.com", "password3", None)
        db.session.commit()

        u_test = User.query.filter_by(username="testuser3").first()
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.email, "testuser3@example.com")
        self.assertNotEqual(u_test.password, "password3")
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        with self.assertRaises(ValueError):
            User.signup(None, "testuser4@example.com", "password4", None)
    
    def test_invalid_email_signup(self):
        with self.assertRaises(ValueError):
            User.signup("testuser5", None, "password5", None)

    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError):
            User.signup("testuser6", "testuser6@example.com", "", None)
        
    def test_valid_authentication(self):
        u = User.authenticate("user1", "password1")
        self.assertIsNotNone(u)

    def test_wrong_password(self):
        self.assertFalse(User.authenticate("user1", "badpassword"))

