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
                return e.args[0], 404

        return wrapper

    return decorator


def verify_invalid_keys(expected_keys: list = DEFAULT_KEYS):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            errors = []
            try:
                for key in data:
                    if not key in expected_keys:
                        errors.append(key)
                        raise KeyError(
                            {
                                "error": "wrong key(s)",
                                "expected keys": list(expected_keys),
                                "received key(s)": list(data),
                                "wrong key(s)": list(errors),
                            }
                        )
                return func(*args, **kwargs)
            except (KeyError, TypeError) as e:
                return e.args[0], 404

        return wrapper

    return decorator


def verify_id():
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            id = kwargs.get("id")
            posts_length = len(list(Post.get_all()))
            try:
                if id <= 0 or id > posts_length:
                    raise IndexError
                return func(*args, **kwargs)
            except IndexError:
                return {"error": "id not found in database."}, 404

        return wrapper

    return decorator
