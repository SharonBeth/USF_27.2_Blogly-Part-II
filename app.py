"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User, Post
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)
db.create_all()

# app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)

@app.route("/")
def user_list():
    """Displays user listing page. Main page"""

    users = User.query.all()
    return render_template('user_list.html', users=users)

@app.route("/create_user")
def enter_user():
    return render_template('create_user.html')

@app.route("/create_user", methods=["POST"])
def create_user():
    """Displays create_user page. """
    first_name = request.form['first_name']
    last_name  = request.form['last_name']
    image_url  = request.form['image_url']
    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()
    return redirect("/")

@app.route("/user_details/<int:user_id>")
def user_details(user_id):
    """Displays create_user page. """
    users=User.query.get(user_id)
    posts=Post.query.filter_by(user_id= user_id).all()
    return render_template('user_details.html', users=users, posts=posts)

@app.route("/edit_user/<int:user_id>")
def edit_user_page(user_id):
    """Go to Edit page"""
    user=User.query.get(user_id)
    return render_template('edit_user.html', user=user)

@app.route("/edit_user/<int:user_id>", methods=["POST"])
def edit_user_post(user_id):
    """Edit the chosen user"""
    update_user = User.query.get_or_404(user_id)
    update_user.first_name = request.form['first_name']
    update_user.last_name  = request.form['last_name']
    update_user.image_url  = request.form['image_url']

    db.session.add(update_user)
    db.session.commit()
    flash (f"User {update_user.first_name} {update_user.last_name} has been edited.")
    return redirect('/')

@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    """Edit the chosen user"""
    user=User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return redirect("/")

@app.route("/new_post/<int:user_id>")
def enter_post(user_id):
    user=User.query.get(user_id)

    return render_template('new_post.html', user_id=user_id, user=user)

@app.route("/new_post/<int:user_id>", methods=["POST"])
def post_the_post(user_id):
    """Displays create_user page. """
    title = request.form['title']
    content  = request.form['content']
    user_id=user_id
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return redirect("/")


@app.route("/post_details/<int:post_id>")
def post_details(post_id):
    """Displays create_user page. """
    # a = Post.query.get(1)
    post=Post.query.get(post_id)
    return render_template('post_details.html', post=post)

@app.route("/edit_post/<int:post_id>")
def edit_post_view(post_id):
    """View the Edit page of the Post"""
    post=Post.query.get(post_id)
    return render_template('edit_post.html', post=post)


@app.route("/edit_post/<int:post_id>", methods=["POST"])
def edit_post(post_id):
    """Submit the changes to the Post selected."""
    update_post = Post.query.get_or_404(post_id)
    update_post.title = request.form['title']
    update_post.content  = request.form['content']

    db.session.add(update_post)
    db.session.commit()

    return redirect('/')

@app.route("/delete_post/<int:post_id>")
def delete_post(post_id):
    """Delete post"""
    delete_post = Post.query.get_or_404(post_id)
    db.session.delete(delete_post)
    db.session.commit()

    return redirect('/')