from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test for model for Users."""

    def setUp(self):
        """Clean up any existing users"""

        User.query.delete()
    
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    
    def test_get_user_by_id(self):
        
        db.drop_all()
        db.create_all()
        user = User(first_name="Tabbitha", last_name="Fahler", image_url="https://cdn.pixabay.com/photo/2017/02/15/12/12/cat-2068462__480.jpg")
        db.session.add(user)
        db.session.commit()

        users = Pet.get_by_user_id('1')

        self.assertEquals(users, [user])
