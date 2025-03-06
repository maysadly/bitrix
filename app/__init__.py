from flask import Flask
import logging
from logging.handlers import RotatingFileHandler
import os
from config import active_config

def create_app(config_object=None):
    """Создание и настройка Flask"""
    app = Flask(__name__, instance_relative_config=True)
    
    
    if config_object is None:
        app.config.from_object(active_config)
    else:
        app.config.from_object(config_object)
    
    
    setup_logging(app)
    
    
    from app.routes.webhooks import webhook_bp
    app.register_blueprint(webhook_bp)
    
    return app

def setup_logging(app):
    """Настройка логирования"""
    log_level = getattr(logging, app.config['LOG_LEVEL'])
    log_format = app.config['LOG_FORMAT']
    
    
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    
    file_handler = RotatingFileHandler('logs/bitrix_webhook.log', maxBytes=10485760, backupCount=10)
    file_handler.setFormatter(logging.Formatter(log_format))
    file_handler.setLevel(log_level)
    
    
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    console_handler.setLevel(log_level)
    
    
    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(log_level)