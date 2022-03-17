from flask import jsonify, request

from app.models.post_model import Post


def create():
    data = request.get_json()

    post = Post(**data)

    post.create_new()

    Post.serialize(post)

    return post.__dict__, 201


def get_all():
    all_posts = Post.get_all()

    posts_list = list(all_posts)

    for post in posts_list:
        Post.serialize(post)

    return jsonify(posts_list), 200


def get_one(post_id: int):
    filtered_post = Post.get_by_id(post_id)

    if not filtered_post:
        raise IndexError

    Post.serialize(filtered_post)

    return filtered_post, 200


def patch(post_id: int):
    data = request.get_json()

    updated_post = Post.patch_by_id(post_id, data)

    if not updated_post:
        raise IndexError

    Post.serialize(updated_post)

    return updated_post, 200


def delete(post_id: int):
    deleted_post = Post.delete_by_id(post_id)

    if not deleted_post:
        raise IndexError

    Post.serialize(deleted_post)

    return deleted_post, 200
