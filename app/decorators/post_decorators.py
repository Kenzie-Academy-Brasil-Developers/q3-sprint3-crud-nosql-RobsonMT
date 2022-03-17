from functools import wraps
from typing import Callable
from flask import request

from app.models.post_model import Post

DEFAULT_KEYS = ["title", "author", "tags", "content"]


def verify_post_keys(expected_keys: list = DEFAULT_KEYS):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            body_req = request.get_json()
            invalid_keys = set(expected_keys).difference(body_req)

            try:
                if invalid_keys:
                    raise KeyError(
                        {
                            "error": "wrong key(s)",
                            "expected": list(expected_keys),
                            "received": list(body_req),
                        }
                    )
                return func(*args, **kwargs)
            except (KeyError, TypeError) as e:
                return e.args[0], 400

        return wrapper

    return decorator


def verify_invalid_keys(expected_keys: list = DEFAULT_KEYS):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            key_error = [key for key in data if not key in expected_keys]

            try:
                if key_error:

                    raise KeyError(
                        {
                            "error": "wrong key(s)",
                            "expected keys": list(expected_keys),
                            "received key(s)": list(data),
                            "wrong key(s)": list(key_error),
                        }
                    )
                return func(*args, **kwargs)
            except (KeyError, TypeError) as e:
                return e.args[0], 400

        return wrapper

    return decorator


def verify_id():
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            id = kwargs.get("id")
            all_posts_list = list(Post.get_all())
            post_with_id = [post for post in all_posts_list if post["id"] == id]

            try:
                if not post_with_id:
                    raise IndexError
                return func(*args, **kwargs)
            except IndexError:
                return {"error": f"id {id} not found in database."}, 404

        return wrapper

    return decorator
