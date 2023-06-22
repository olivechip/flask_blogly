from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

"""Models for Blogly."""

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    image_url = db.Column(db.String, default = "https://static.vecteezy.com/system/resources/thumbnails/009/734/564/small/default-avatar-profile-icon-of-social-media-user-vector.jpg")

    @classmethod
    def order_by_last_first(cls):
        return cls.query.order_by(User.last_name, User.first_name).all()

    def __repr__(self):
        u = self
        return f"id={u.id} first_name={u.first_name} last_name={u.last_name}"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.Text(300), nullable = False)
    content = db.Column(db.Text(40000), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False)
    op = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='post')