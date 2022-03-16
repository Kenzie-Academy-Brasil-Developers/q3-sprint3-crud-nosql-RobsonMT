from distutils.log import error
from app.models.post_model import Post
from flask import jsonify


def retrieve():
    posts_list = Post.get_all()
    posts_list = list(posts_list)

    for post in posts_list:
        del post["_id"]

    return jsonify(posts_list), 200


def verify_unexpected_keys(data):
    keys = ["title", "author", "tags", "content"]
    errors = []

    for key in data:
        if not key in keys:
            errors.append(key)
            raise KeyError(
                {
                    "error": "wrong key(s)",
                    "expected keys": list(keys),
                    "received key(s)": list(data),
                    "wrong key(s)": list(errors),
                }
            )
