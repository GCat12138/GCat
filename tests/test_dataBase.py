import unittest
from flask import current_app
from app import create_app, db
from app import models
from app.models import User, Address

class DatabaseTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_insert(self):
        user1 = User()
        user1.nickName = 'jjj'
        user1.phoneNumber = '13580502860'
        db.session.add(user1)
        db.session.commit()

        q_user = User.query.filter_by(phoneNumber='13580502860').first()

        self.assertFalse( q_user is None)
