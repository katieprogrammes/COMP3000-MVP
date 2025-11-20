from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
from routes import bp as routes_bp 

app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Registering the blueprint
app.register_blueprint(routes_bp)

'''
with app.app_context():
    db.create_all()
'''                  

if __name__ == "__main__":
    app.run(debug=True)