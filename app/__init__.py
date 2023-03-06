from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate



#Initializing Section
app = Flask(__name__)
app.config.from_object(Config)

login = LoginManager(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login.login_view = 'login'
login.login_message = 'You must be logged in to view this page'
login.login_message_category = 'warning'

from app import routes, models

