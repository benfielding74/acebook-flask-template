from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from acebook.auth import login_required
from acebook.db import get_db
from acebook.post import Post
from acebook.post import Comment

bp = Blueprint('posts', __name__)

@bp.route('/')
def index():
    posts = Post.all()

    comments = Comment.all_comments()
    return render_template('posts/index.html', posts=posts, comments = comments)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if not body:
            error = 'Type something you would like to post!'

        if error is not None:
            flash(error)
        else:
            Post.create(title, body, g.user.id, g.user.profile_picture)
            return redirect(url_for('posts.index'))

    return render_template('posts/create.html')

@bp.route('/upload_photo', methods=('GET', 'POST'))
@login_required
def upload_photo():
    if request.method == 'POST':
        caption = request.form['caption']
        photo = request.files['file']
        images_path = current_app.instance_path.replace("instance","acebook/static/images")
        profile_picture_path = os.path.join(images_path,secure_filename(photo.filename))
        photo.save(profile_picture_path)
        error = None

        if not caption:
            error = "Don't you want a caption."

        if not photo:
            error = 'Whats the point if you not putting a picture on?'

        if error is not None:
            flash(error)
        else:
            Post.create(caption, photo, g.user.id, g.user.profile_picture)
            return redirect(url_for('posts.index'))

    return render_template('posts/upload_photo.html')

@bp.route('/cancel', methods=('POST',))
@login_required
def cancel():
    return redirect(url_for('posts.index'))

def get_post(id, check_author=True):
    post = Post.find_by_id(id)

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post.author_id != g.user.id:
        abort(403)

    return post

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            post.update(title, body, id)
            return redirect(url_for('posts.index'))

    return render_template('posts/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    post = Post.find_by_id(id)
    post.delete()

    return redirect(url_for('posts.index'))

@bp.route('/<int:id>/like_post', methods=('POST',))
@login_required
def like_post(id):
    post = Post.find_by_id(id)
    post.like_post()
    return redirect(url_for('posts.index'))

@bp.route('/<int:id>/add_comment', methods=('POST', 'GET'))
@login_required
def add_comment(id):
    comment = request.form['comment']
    post = Post.find_by_id(id)
    post.add_comment(comment, id, g.user.id)
    return redirect(url_for('posts.index'))
