import os

from flask import Flask, render_template, jsonify
from flask import request, abort
from flask_sqlalchemy import SQLAlchemy

NUM_PER_PAGE = 4

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URL')
db = SQLAlchemy(app)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String)
    posted_at = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Post id={self.id}, title={self.title}>"

    def serialize(self):
        return {'id': self.id,
                'title': self.title,
                'body': self.body,
                'posted_at': self.posted_at
                }


@app.route('/posts/')
def post_index():
    page_num = int(request.args.get('page') or '1')
    post_objs = Post.query.order_by(Post.id.desc()).paginate(page_num, NUM_PER_PAGE)
    return render_template('posts/index.html', posts=post_objs.items)


@app.route('/posts/<post_id>')
def post_show(post_id):
    int_post_id = int(post_id) # yes yes yes, sql injection
    post = Post.query.get_or_404(int_post_id)
    return render_template('posts/show.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)

