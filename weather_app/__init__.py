from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)  # Импорт параметров конфигурации

    from weather_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    db.init_app(app)
    with app.app_context():
        db.create_all()  # Инициализация БД

    return app

from weather_app import models
