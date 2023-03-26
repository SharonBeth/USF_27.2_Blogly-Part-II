"""Blogly application."""


from models import db, connect_db, User, Post, Tag, PostTag
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask import Flask, render_template, request, redirect, flash
# from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.app_context().push()
connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = "SECRET!"
# debug = DebugToolbarExtension(app)


######## User routes############
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

#######################Post routes#########################################

@app.route("/new_post/<int:user_id>")
def enter_post(user_id):
    user=User.query.get(user_id)
    tags=Tag.query.all()
    return render_template('new_post.html', user_id=user_id, user=user, tags=tags)

@app.route("/new_post/<int:user_id>", methods=["POST"])
def post_the_post(user_id):
    """Displays create_user page. """
    # title = request.form['title']
    # content  = request.form['content']
    # user_id=user_id
    # post = Post(title=title, content=content, user_id=user_id)
    # db.session.add(post)
    # db.session.commit()
    # return redirect("/")

    user=User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'],
                    content=request.form['content'],
                    user=user,
                    tags=tags)
    db.session.add(new_post)
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
    tags=Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)


@app.route("/edit_post/<int:post_id>", methods=["POST"])
def edit_post(post_id):
    """Submit the changes to the Post selected."""
    update_post = Post.query.get_or_404(post_id)
    update_post.title = request.form['title']
    update_post.content  = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    update_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(update_post)
    db.session.commit()

    return redirect('/')

@app.route("/delete_post/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    delete_post = Post.query.get_or_404(post_id)
    db.session.delete(delete_post)
    db.session.commit()

    return redirect('/')

############################Tag routes################################

@app.route('/tags')
def tags_index():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tag_list.html', tags=tags)


@app.route('/tags/new')
def tags_new_form():
    """Show a form to create a new tag"""

    posts = Post.query.all()
    return render_template('create_tag.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Handle form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()
    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('edit_tag.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle form submission for deleting an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")