from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from extenstions import db, login_manager
from routes import bp as routes_bp
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)
login_manager.login_view = "routes.login"
login_manager.login_message_category = "danger"

#Registering the blueprint
app.register_blueprint(routes_bp)

'''
with app.app_context():
    db.create_all()
'''                 



if __name__ == "__main__":
    app.run(debug=True)