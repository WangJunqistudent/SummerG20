from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__, template_folder='main/static/templates')

from main import routes

db = SQLAlchemy()

def create_app():
    app.config.from_pyfile('config.py')
    db.init_app(app)

    from main.routes import main_bp
    app.register_blueprint(main_bp)

    return app
