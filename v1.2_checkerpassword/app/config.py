import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from os import environ

# Inisialisasi db di level global
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
    
    # Inisialisasi db dengan app
    db.init_app(app)
    
    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["20 per minute"],
        storage_uri="redis://redis:6379/0"
    )
    
    return app, limiter