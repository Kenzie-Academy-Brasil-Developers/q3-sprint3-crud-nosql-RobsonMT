def post_route(app):
    @app.post("/posts")
    def create_post():
        ...

    @app.delete("/posts/<int:id>")
    def delete_post():
        ...

    @app.get("/posts/<int:id>")
    def ready_post_by_id():
        ...

    @app.get("/post")
    def read_posts():
        ...

    @app.patch("/posts/<int:id>")
    def update_post():
        ...
