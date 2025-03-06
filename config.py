import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    """Базовая конфигурация"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    FIRST_CRM_URL = os.getenv("FIRST_CRM_URL")
    SECOND_CRM_URL = os.getenv("SECOND_CRM_URL")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
class DevelopmentConfig(Config):
    """Конфигурация для разработки"""
    DEBUG = True
    
class TestingConfig(Config):
    """Конфигурация для тестирования"""
    TESTING = True
    DEBUG = True
    
class ProductionConfig(Config):
    """Конфигурация для продакшна"""
    DEBUG = False
    

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


config_name = os.getenv('FLASK_ENV', 'default')
active_config = config[config_name]