from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Pets."""

    def setUp(self):
        """Add sample user"""
    
        User.query.delete()

        user = User(first_name="TestUser", last_name="Last", image_url="https://cdn.pixabay.com/photo/2017/02/15/12/12/cat-2068462__480.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
    
    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('TestUser', html)

    def test_create_user(self):
        with app.test_client() as client:
            d = {"first_name": "Reese", "last_name": "Fahler", "image_url": "https://cdn.pixabay.com/photo/2017/02/15/12/12/cat-2068462__480.jpg"}
            resp = client.post("/create_user", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("<li><a href=/user_details/2> Reese Fahler</li>", html)
        
    def test_individual_user(self):
        with app.test_client() as client:
            resp = client.get(f"/user_details/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
    

