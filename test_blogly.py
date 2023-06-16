from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Clean up any existing users."""
        User.query.delete()

        user = User(first_name="TestFirstName", last_name="TestLastName", image_url="https://tinyurl.com/eae48wfs")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up failed transactions."""
        db.session.rollback()
    
    def test_home_page(self):
        with app.testclient() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Welcome to Blogly!', html)
    
            