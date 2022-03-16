from flask import jsonify

from app.models.post_model import Post


def retrieve():
    posts_list = Post.get_all()
    posts_list = list(posts_list)

    for post in posts_list:
        del post["_id"]

    return jsonify(posts_list), 200
