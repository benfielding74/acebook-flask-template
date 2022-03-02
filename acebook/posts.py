from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from acebook.auth import login_required
from acebook.db import get_db
from acebook.post import Post

bp = Blueprint('posts', __name__)

@bp.route('/')
def index():
    posts = Post.all()
    return render_template('posts/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            Post.create(title, body, g.user.id)
            return redirect(url_for('posts.index'))

    return render_template('posts/create.html')

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