from functools import wraps
from http import HTTPStatus
from typing import Callable
from flask import request

DEFAULT_KEYS = ["title", "author", "tags", "content"]


def verify_keys(expected_keys: list = DEFAULT_KEYS):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **wargs):
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
                return func()
            except (KeyError, TypeError) as e:
                return e.args[0], HTTPStatus.BAD_REQUEST

        return wrapper

    return decorator
