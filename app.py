"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = "my_secret_key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
app.app_context( ).push( )
db.create_all()

@app.route('/')
def home_page():
    """shows the home page"""
    return render_template('home_page.html')

@app.route('/users')
def show_users():
    """shows a list of all users"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def create_user():
    """shows a form w/ input to create a new user"""
    return render_template('create_user.html')

@app.route('/users/new', methods=['POST'])
def added_user():
    """sends the form data to create a user and adds to database"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    flash(f'{first_name} {last_name} has been added!')
    return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user_details(user_id):
    """shows the user details page"""
    user = User.query.get_or_404(user_id)
    return render_template('user_details.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    """shows a form w/ inputs to edit existing user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edited_user(user_id):
    """sends form data to edit user and database"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    old_fn = request.form["old_fn"]
    old_ln = request.form["old_ln"]

    user = User.query.session.get(User, user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url

    db.session.commit()

    flash(f'{old_fn} {old_ln} has been updated to {first_name} {last_name}!')
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """deletes user from database"""
    user = User.query.session.get(User, user_id)
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    flash(f"{user.first_name} {user.last_name} has been deleted!")
    return redirect('/users')