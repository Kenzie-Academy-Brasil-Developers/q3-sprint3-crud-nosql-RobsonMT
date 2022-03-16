from flask import request
from app.controllers.post_controller import retrieve, verify_unexpected_keys
from app.decorators.verify_keys import verify_keys
from app.models.post_model import Post


def post_route(app):
    @app.post("/posts")
    @verify_keys()
    def create_post():
        body_req = request.get_json()

        post = Post(**body_req)
        post.create_new_post()

        return {"msg": "created"}, 201

    @app.delete("/posts/<int:id>")
    def delete_post(id):
        try:
            deleted = Post.delete_by_id(id)
            return deleted, 200
        except (IndexError, TypeError):
            return {"error": "id not found."}, 404

    @app.get("/posts/<int:id>")
    def ready_post_by_id(id):

        try:
            post = Post.get_by_id(id)
            return post, 200
        except (IndexError, TypeError):
            return {"error": "id not found."}, 404

    @app.get("/posts")
    def read_posts():
        return retrieve()

    @app.patch("/posts/<int:id>")
    def update_post(id):
        body_req = request.get_json()

        try:
            verify_unexpected_keys(body_req)
            updated = Post.patch_by_id(id, body_req)
            return updated, 200
        except (KeyError, TypeError) as e:
            return e.args[0], 404
