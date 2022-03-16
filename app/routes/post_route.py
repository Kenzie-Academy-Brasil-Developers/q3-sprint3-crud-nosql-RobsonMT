from flask import request

from app.controllers.post_controller import retrieve
from app.decorators.verify_keys import verify_invalid_keys
from app.decorators.verify_keys import verify_post_keys
from app.decorators.verify_keys import verify_id
from app.models.post_model import Post


def post_route(app):
    @app.post("/posts")
    @verify_post_keys()
    def create_post():
        post = Post(**request.get_json())
        return post.create_new(), 201

    @app.delete("/posts/<int:id>")
    @verify_id()
    def delete_post(id):
        return Post.delete_by_id(id), 200

    @app.get("/posts/<int:id>")
    @verify_id()
    def search_post(id):
        return Post.get_by_id(id), 200

    @app.get("/posts")
    def read_posts():
        return retrieve()

    @app.patch("/posts/<int:id>")
    @verify_invalid_keys()
    @verify_id()
    def update_post(id):
        body_req = request.get_json()
        return Post.patch_by_id(id, body_req), 200
