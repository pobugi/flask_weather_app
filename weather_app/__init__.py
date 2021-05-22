import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)  # Импорт параметров конфигурации

    from weather_app.main import bp as main_bp
    app.register_blueprint(main_bp)

    handler = RotatingFileHandler(app.config['LOGFILE'],
                                  maxBytes=1000000, backupCount=1)
    logging.basicConfig(level=logging.DEBUG)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s'))
    app.logger.addHandler(handler)

    db.init_app(app)
    with app.app_context():
        db.create_all()  # Инициализация БД

    return app


from weather_app import models
