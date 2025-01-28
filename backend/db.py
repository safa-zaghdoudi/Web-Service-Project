from flask_pymongo import PyMongo

# MongoDB instance
mongo = PyMongo()

def init_db(app):
    """
    Initializes the MongoDB connection using the Flask app configuration.
    """
    mongo.init_app(app)
