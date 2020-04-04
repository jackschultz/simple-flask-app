import os

from flask import Flask
from flask import request, abort

from sqlalchemy import create_engine

NUM_PER_PAGE = 4
DB_URL = os.environ.get('DB_URL')

engine = create_engine(DB_URL)

app = Flask(__name__)


@app.route('/posts/')
def post_index():
    page = int(request.args.get('page') or '0')
    index = (NUM_PER_PAGE + 1) - (NUM_PER_PAGE * page)
    offset = NUM_PER_PAGE * index if index > 0 else 1000 # never going to have 4000 posts

    with engine.connect() as connection:
        result = connection.execute(f"select * from posts order by id desc limit {NUM_PER_PAGE} offset {offset}").fetchall()
        pages = [dict(res) for res in result]

    retval = {'posts': pages}
    return retval


@app.route('/posts/<post_id>')
def post_get(post_id):
    int_post_id = int(post_id) # yes yes yes, sql injection
    with engine.connect() as connection:
        post = connection.execute(f"select * from posts where id = {int_post_id}").fetchone()
        return dict(post)


if __name__ == '__main__':
    app.run(debug=True)

