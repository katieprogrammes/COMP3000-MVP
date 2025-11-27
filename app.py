from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from extenstions import db, login_manager
from routes import bp as routes_bp

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)
migrate = Migrate(app, db)

login_manager.init_app(app)

#Registering the blueprint
app.register_blueprint(routes_bp)

'''
with app.app_context():
    db.create_all()
'''                  



if __name__ == "__main__":
    app.run(debug=True)