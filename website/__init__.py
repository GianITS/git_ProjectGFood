from flask import Flask
from pymongo import MongoClient
import certifi

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ProjectITS33'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app