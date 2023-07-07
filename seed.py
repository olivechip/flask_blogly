from models import db, User, Post
from app import app

db.drop_all()
db.create_all()

"""Sample Users"""
kitty = User(first_name='Kitty', last_name='Smalls', image_url='https://bestfriends.org/sites/default/files/story_images/Smooches_courtesyofJaNaeGoodrich.jpg')
puppy = User(first_name='Puppy', last_name='Biggs', image_url='https://media-cldnry.s-nbcnews.com/image/upload/rockcms/2023-03/puppy-dog-mc-230321-03-b700d4.jpg')
db.session.add_all([kitty, puppy])
db.session.commit()

"""Sample Posts"""
post1 = Post(title='All Alone', content="sometimes i'm alone, sometimes i'm not", created_at=db.func.now(), op=1)
post2 = Post(title='catjam', content="meow~ meow~ meow~!!!", created_at=db.func.now(), op=1)
post3 = Post(title='Dear Owner', content="Are you going to feed me?!", created_at=db.func.now(), op=2)
post4 = Post(title='Steamed Hams', content="I smell bacon! I want bacon!!", created_at=db.func.now(), op=2)
