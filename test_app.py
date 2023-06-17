from unittest import TestCase
import json

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

        user = User(first_name="TestFirstName", last_name="TestLastName")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user_fn = user.first_name
        self.user_ln = user.last_name

    def tearDown(self):
        """Clean up failed transactions."""
        db.session.rollback()
    
    def test_home_page(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Welcome to Blogly!', html)
    
    def test_show_users(self):
        with app.test_client() as client:
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Users', html)

    def test_create_user(self):
        with app.test_client() as client:
            res = client.get('/users/new')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Create a User', html)

    # def test_added_user(self):
    #     with app.test_client() as client:
    #         # test post/add data was sent and redirected
    #         data = {'first_name': 'TestFirstName', 'last_name': 'TestLastName'}
    #         res = client.post('/users/new', data=data)
    #         self.assertIn(res.status_code, [200, 302])

    #         # test redirect to /users
    #         res = client.get('/users')
    #         html = res.get_data(as_text=True)
    #         self.assertEqual(res.status_code, 200)
    #         self.assertIn('TestFirst TestLast has been added!', html)
    
    def test_show_user_details(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"{self.user_fn} {self.user_ln}", html)
        
            res = client.get(f'/users/-{self.user_id}')
            self.assertEqual(res.status_code, 404)

    def test_edit_user(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user_id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"Edit a User", html)

            res = client.get(f'/users/-{self.user_id}')
            self.assertEqual(res.status_code, 404)

    # def test_edited_user(self):
    #     with app.test_client() as client:

    #         # test post/edit data was sent and redirected
    #         data = {'first_name': self.user_fn, 'last_name': self.user_ln}
    #         res = client.post(f'/users/{self.user_id}/edit', data=data)
    #         self.assertEqual(res.status_code, 302)

    #         # test redirect to /users
    #         res = client.get('/users')
    #         html = res.get_data(as_text=True)

    #         self.assertEqual(res.status_code, 200)
    #         self.assertIn('has been updated', html)

    def test_delete_user(self):
        with app.test_client() as client:

            # test post/delete data was sent and redirected
            res = client.post(f'/users/{self.user_id}/delete')
            self.assertEqual(res.status_code, 302)

            # test redirect to /users
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'{self.user_fn} {self.user_ln} has been deleted!', html)