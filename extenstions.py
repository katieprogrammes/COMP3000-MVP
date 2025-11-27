from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


#Fixing circular imports
db = SQLAlchemy()
login_manager = LoginManager()
