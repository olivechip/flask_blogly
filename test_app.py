from unittest import TestCase

from app import app
from models import db, User, Post

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

        user = User(first_name="TestFirstName", last_name="TestLastName", image_url="https://media-cldnry.s-nbcnews.com/image/upload/rockcms/2023-03/puppy-dog-mc-230321-03-b700d4.jpg")
        db.session.add(user)
        db.session.commit()

        self.user = user

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

    def test_added_user(self):
        with app.test_client() as client:

            # test post/add data was sent and redirected
            data = {'first_name': self.user.first_name, 'last_name': self.user.last_name,
                    'image_url': 'https://media-cldnry.s-nbcnews.com/image/upload/rockcms/2023-03/puppy-dog-mc-230321-03-b700d4.jpg'}
            res = client.post('/users/new', data=data)
            self.assertIn(res.status_code, [200, 302])

            # test redirect to /users
            res = client.get('/users')
            html = res.get_data(as_text=True)
            self.assertIn(res.status_code, [200, 302])
            self.assertIn(f'{self.user.get_full_name()} has been added!', html)
    
    def test_show_user_details(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user.id}')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"{self.user.get_full_name()}", html)
        
            res = client.get(f'/users/-{self.user.id}')
            self.assertEqual(res.status_code, 404)

    def test_edit_user(self):
        with app.test_client() as client:
            res = client.get(f'/users/{self.user.id}/edit')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f"Edit a User", html)

            res = client.get(f'/users/-{self.user.id}')
            self.assertEqual(res.status_code, 404)

    def test_edited_user(self):
        with app.test_client() as client:

            # test post/edit data was sent and redirected
            data = {'first_name': self.user.first_name, 'last_name': self.user.last_name, 
                    'image_url': 'https://media-cldnry.s-nbcnews.com/image/upload/rockcms/2023-03/puppy-dog-mc-230321-03-b700d4.jpg', 
                    'old_fn': 'OldTestFN', 'old_ln': 'OldTesLN'}

            res = client.post(f'/users/{self.user.id}/edit', data=data)
            self.assertEqual(res.status_code, 302)

            # test redirect to /users
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'has been updated to {self.user.get_full_name()}!', html)

    def test_delete_user(self):
        with app.test_client() as client:

            # test post/delete data was sent and redirected
            res = client.post(f'/users/{self.user.id}/delete')
            self.assertEqual(res.status_code, 302)

            # test redirect to /users
            res = client.get('/users')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn(f'{self.user.get_full_name()} has been deleted!', html)

# class PostViewsTestCase(TestCase):
#     """Tests for model for Posts."""

#     def setUp(self):
#         """Clean up any existing posts."""
#         Post.query.delete()

#         post = Post(title="test_title", content="test_content", created_at=db.func.now(), op=1)
#         db.session.add(post)
#         db.session.commit()

#         self.post = post

#     def tearDown(self):
#         """Clean up failed transactions."""
#         db.session.rollback()

#     def test_add_post(self):
#         with app.test_client() as client:

#             res = client.get(f'/users/{self.post.op}/posts/new')
#             self.assertEqual(res.status_code, 200)

#     def test_added_post(self):
#         with app.test_client() as client:

#             data = {'title': self.post.title, 
#                 'content': self.post.content, 
#                 'created_at': self.post.created_at, 
#                 'op': self.post.op}

#             res = client.post(f'/users/{self.post.op}/posts/new', data=data)
#             self.assertEqual(res.status_code, 200)
#             self.assertEqual(res.status_code, 302)
