from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


app = Flask(__name__)


app.config["SECRET_KEY"] = "dawdAHDWAWhabdwadgya"
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
db = SQLAlchemy(app)


login_manager = LoginManager(app)