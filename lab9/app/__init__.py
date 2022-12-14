
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from config import config
import logging
logging.basicConfig(filename='app.log', encoding='UTF-8', filemode='a', format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


# app = Flask(__name__)
# app.config.from_object('config')

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'account.login'
login_manager.login_message_category = 'info'


def create_app(config_name = 'default'):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))

    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app.home import home_bp
        from app.candidate_form import candidate_bp
        from app.account import account_bp
        
        app.register_blueprint(home_bp)
        app.register_blueprint(candidate_bp, url_prefix='/candidate')
        app.register_blueprint(account_bp)

    return app
