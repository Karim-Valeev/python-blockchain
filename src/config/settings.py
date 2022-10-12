import os

from pydantic import BaseSettings

from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


class Settings(BaseSettings):
    ARBITER_URL = os.environ.get("ARBITER_URL", "http://89.108.115.118")

    LOG_LEVEL: str = os.environ.get('LOG_LEVEL', 'INFO')
    LOGGER_NAME: str = 'app_logger'
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)s %(name)s %(funcName)s %(message)s %(pathname)s %(lineno)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': LOG_LEVEL,
            },
        },
        'loggers': {
            'app_logger': {
                'handlers': ['console'],
                'level': LOG_LEVEL,
            },
        }
    }


settings = Settings()
