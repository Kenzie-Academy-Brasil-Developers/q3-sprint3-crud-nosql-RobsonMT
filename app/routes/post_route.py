from app.decorators import verify_invalid_keys
from app.decorators import verify_post_keys
from app.decorators import verify_id
from app.controllers import post_controller


def post_route(app):
    @app.post("/posts")
    @verify_post_keys()
    def create_post():
        return post_controller.create()

    @app.delete("/posts/<int:id>")
    @verify_id()
    def delete_post(id):
        return post_controller.delete(id)

    @app.get("/posts/<int:id>")
    @verify_id()
    def find_post(id):
        return post_controller.get_one(id)

    @app.get("/posts")
    def read_posts():
        return post_controller.get_all()

    @app.patch("/posts/<int:id>")
    @verify_invalid_keys()
    @verify_id()
    def update_post(id):
        return post_controller.patch(id)
