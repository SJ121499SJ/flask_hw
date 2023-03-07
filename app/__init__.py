from flask import Flask
from config import Config
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


login = LoginManager()
db = SQLAlchemy()
migrate = Migrate()



def create_app():
    #Initializing Section
    app = Flask(__name__)
    app.config.from_object(Config)
    
    login.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    
    login.login_view = 'login'
    login.login_message = 'You must be logged in to view this page'
    login.login_message_category = 'warning'
    
    from app.blueprints.main import main
    from app.blueprints.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app



