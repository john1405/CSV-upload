import os

# i have used general variables here you can change according to your system
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "your_secret_key") # you can put your secret keys here
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your_jwt_secret_key")
    MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/imdb")
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")