from flask import Flask

from app import routes


# Flask Factory
def create_app():
    app = Flask(__name__)

    routes.init_app(app)

    return app
