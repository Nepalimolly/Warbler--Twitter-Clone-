from unittest import TestCase
from sqlalchemy import exc
from models import db, User, Message, Follows, Likes

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """Test views for messages."""

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///warbler-test'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        return app

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            self.u1 = User.signup("user1", "user1@example.com", "password1", None)
            self.u2 = User.signup("user2", "user2@example.com", "password2", None)

            db.session.commit()

            self.u1 = User.query.filter_by(username='user1').first()
            self.u2 = User.query.filter_by(username='user2').first()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_message_model(self):
        """Does basic model work?"""
        
        m = Message(
            text="a warble",
            user_id=self.uid
        )

        db.session.add(m)
        db.session.commit()

        # User should have 1 message
        self.assertEqual(len(self.u.messages), 1)
        self.assertEqual(self.u.messages[0].text, "a warble")

    def test_message_likes(self):
        m1 = Message(
            text="a warble",
            user_id=self.uid
        )

        m2 = Message(
            text="a very interesting warble",
            user_id=self.uid 
        )

        u = User.signup("testuser2", "testuser2@test.com", "password2", None)
        uid = 88888
        u.id = uid
        db.session.add_all([m1, m2, u])
        db.session.commit()

        u.likes.append(m1)

        db.session.commit()

        l = Likes.query.filter(Likes.user_id == uid).all()
        self.assertEqual(len(l), 1)
    
