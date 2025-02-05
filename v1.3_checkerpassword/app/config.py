import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ

# Inisialisasi db di level global
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')

    # Inisialisasi db dengan app
    db.init_app(app)

    return app 
