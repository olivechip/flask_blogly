from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

default_pfp = "https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small/default-avatar-profile-icon-of-social-media-user-vector.jpg"

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    image_url = db.Column(db.String, default = default_pfp)

    posts = db.relationship('Post', backref='user', cascade='all, delete-orphan')    
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def order_by_last_first(cls):
        return cls.query.order_by(User.last_name, User.first_name).all()

    def __repr__(self):
        u = self
        return f"id={u.id} first_name={u.first_name} last_name={u.last_name}"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text, nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)
    op = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)

    @property
    def friendly_date(self):
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")

    @classmethod
    def show_recent(cls):
        return cls.query.order_by(Post.created_at.desc()).limit(5).all()

class PostTag(db.Model):
    __tablename__ = 'post_tags'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key = True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key = True)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.Text, nullable = False, unique = True)

    @classmethod
    def alphabetical(cls):
        return cls.query.order_by(Tag.name).all()

    posts = db.relationship('Post', secondary='post_tags', backref='tags', cascade='all, delete')