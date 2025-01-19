from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from ressources.residency import ResidencyBlueprint
from ressources.auth import auth

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Application Configuration
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Residency API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.register_blueprint(auth, url_prefix="/auth")    #import the auth blueprint and initialize it
    app.config["SECRET_KEY"] = "a13ce7904227e39f15528a97bd437bd04428266e39f8f31579b45bf957165327"    # include a secret key for JWT

    # MongoDB Setup
    client = MongoClient("mongodb+srv://zaghdoudisafe:4T6p7FyUp8DudtEn@cluster0.pgrad.mongodb.net")
    app.db = client["residency_db"]  # Attach the database to the Flask app for use in other parts

    # Register Residency Blueprint
    app.register_blueprint(ResidencyBlueprint, url_prefix="/residencies")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)