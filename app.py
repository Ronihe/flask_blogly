"""Blogly application."""

from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = 'SUPER MEGA HYPER SECRET'
DebugToolbarExtension(app)
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False


@app.route('/')
def display_homepage():
    """redirec to the page displaying all users in the Blogly database"""

    return redirect("/users")


@app.route('/users')
def display_all_users():
    """Displays all users in the Blogly database"""

    users = User.query.order_by(User.last_name.asc(),
                                User.first_name.asc()).all()
    return render_template("homepage.html", users=users)


@app.route('/users', methods=["POST"])
def make_a_new_user():
    """ make a new user"""

    form = request.form
    new_user = User(
        first_name=form["first_name"],
        last_name=form["last_name"],
        image_url=form["image_url"])

    db.session.add(new_user)
    db.session.commit()
    flash(f"You made {new_user.first_name} {new_user.last_name}!")
    return redirect("/users")


@app.route('/users/new')
def display_new_user_form():
    """display new user form"""

    return render_template("new_user.html")


@app.route('/users/<int:user_id>')
def display_a_user(user_id):
    """display a user according to its id"""

    user = User.query.get(user_id)
    print(request.args)
    return render_template("user.html", user=user)


@app.route('/users/<int:user_id>/edit')
def display_editing_form(user_id):
    """display editing a user form"""

    user = User.query.get(user_id)
    return render_template("edit_user.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def process_editing_form(user_id):
    """process editing a user form"""

    form = request.form
    user = User.query.get_or_404(user_id)

    user.first_name = form.get("first_name", None) or user.first_name
    user.last_name = form.get("last_name", None) or user.last_name
    user.image_url = form.get("image_url", None) or user.image_url
    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_a_user(user_id):
    """delete a user by its id"""

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'you deeted me! {user.first_name} {user.last_name}')

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def display_new_post_form(user_id: int):

    return render_template('new_post.html', user=User.query.get(user_id))


@app.route('/users/<int:user_id>/posts', methods=['POST'])
def process_new_post_form(user_id: int):
    form = request.form
    new_post = Post(
        title=form['title'], content=form['content'], user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def display_post(post_id: int):
    return render_template('post.html', post=Post.query.get(post_id))


@app.route('/posts/<int:post_id>', methods=['POST'])
def delete_post(post_id: int):
    post = Post.get(post_id)
    user_id = post.user.id
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>/edit')
def display_edit_post_form(post_id: int):
    return render_template('edit_post.html', post=Post.query.get(post_id))


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def process_edit_post_form(post_id: int):
    form = request.form
    post = Post.query.get(post_id)
    post.title = form.get('title')
    post.content = form.get('content')
    db.session.add(post)
    db.session.commit()
    flash("post edited!")
    return redirect(f"/posts/{post_id}")
