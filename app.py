"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

app.config['SECRET_KEY'] = "my_secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context().push()
db.create_all()

@app.route('/')
def home_page():
    """shows the home page"""
    posts = Post.show_recent()
    return render_template('home_page.html', posts=posts)

@app.route('/users')
def show_users():
    """shows a list of all users"""
    users = User.order_by_last_first()
    return render_template('users.html', users=users)

@app.route('/users/new')
def create_user():
    """shows a form w/ input to create a new user"""
    return render_template('create_user.html')

@app.route('/users/new', methods=['POST'])
def added_user():
    """sends the form data to create a user and adds to database"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    flash(f'{new_user.full_name} has been added!')
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """shows the user details page"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.op == user_id).all()
    return render_template('user_details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """shows a form w/ inputs to edit existing user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edited_user(user_id):
    """sends form data to edit user and database"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    old_fn = request.form['old_fn']
    old_ln = request.form['old_ln']

    user = User.query.session.get(User, user_id)
    user.first_name = first_name
    user.last_name = last_name
    if image_url is None:
        user.image_url = default_pfp
    else:
        user.image_url = image_url

    db.session.commit()

    flash(f'{old_fn} {old_ln} has been updated to {user.full_name}!')
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """deletes user from database"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    flash(f"{user.full_name} has been deleted!")
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """shows form to add new post for user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('add_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def added_post(user_id):
    """sends post data to add post to user and database"""
    title = request.form['post_title']
    content = request.form['post_content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=title, content=content, created_at=db.func.now(), op=user_id, tags=tags)

    db.session.add(new_post)
    db.session.commit()

    flash(f"Post '{new_post.title}' was created!")
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """shows post details"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """shows form to edit post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edited_post(post_id):
    """sends new post data to database and redirects to new post details"""
    title = request.form['post_title']
    content = request.form['post_content']

    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    post = Post.query.session.get(Post, post_id)
    post.title = title
    post.content = content
    post.tags = tags

    db.session.add(post)
    db.session.commit()

    flash(f"Post '{post.title}' was updated!")
    return redirect(f'/posts/{post.id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """deletes post from database"""
    post = Post.query.session.get(Post, post_id)
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    flash(f"Post '{post.title}' was deleted!")
    return redirect(f'/users/{post.op}')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

@app.route('/tags')
def show_tags():
    tags = Tag.alphabetical()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)

@app.route('/tags/new')
def add_tag():
    return render_template('add_tag.html')

@app.route('/tags/new', methods=['POST'])
def added_tag():
    """sends the form data to create a tag and adds to database"""
    try:
        tag_name = request.form['tag_name']

        new_tag = Tag(name=tag_name)
        db.session.add(new_tag)
        db.session.commit()

        flash(f'{new_tag.name} has been added!')
        return redirect('/tags')

    except: 
        db.session.rollback()

        flash(f"'{new_tag.name}' already exists as a tag.")
        return redirect('/tags/new')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """shows a form w/ inputs to edit existing tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def edited_tag(tag_id):
    """sends form data to edit tag and database"""
    try:
        tag_name = request.form['tag_name']

        tag = Tag.query.get_or_404(tag_id)
        tag.name = tag_name

        db.session.commit()

        flash(f"Tag '{tag.name}' was updated!")
        return redirect(f'/tags/{tag.id}')

    except: 
        db.session.rollback()

        flash(f"'{tag.name}' already exists as a tag.")
        return redirect(f'/tags/{tag_id}/edit')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """deletes tag from database"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    flash(f"The '{tag.name}' tag has been deleted!")
    return redirect('/tags')