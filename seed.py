from models import db, User, Post, Tag, PostTag
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

db.session.add_all([post1, post2, post3, post4])
db.session.commit()

"""Sample Tags"""
tag1 = Tag(name='funny')
tag2 = Tag(name='dogs')
tag3 = Tag(name='cats')
tag4 = Tag(name='mad')

db.session.add_all([tag1, tag2, tag3, tag4])
db.session.commit()

"""Sample PostTags"""
tp1 = PostTag(post_id='1', tag_id='3')
tp2 = PostTag(post_id='1', tag_id='1')
tp3 = PostTag(post_id='2', tag_id='1')
tp4 = PostTag(post_id='2', tag_id='3')
tp5 = PostTag(post_id='3', tag_id='4')
tp6 = PostTag(post_id='3', tag_id='2')
tp7 = PostTag(post_id='4', tag_id='1')
tp8 = PostTag(post_id='4', tag_id='2')

db.session.add_all([tp1, tp2, tp3, tp4, tp5, tp6, tp7, tp8])
db.session.commit()

