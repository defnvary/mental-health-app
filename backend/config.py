import os

class Config:
    # PostgreSQL configuration - UPDATE THESE WITH YOUR CREDENTIALS
    SQLALCHEMY_DATABASE_URI = 'postgresql://mha_user:mha_pass@localhost:5432/mha'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'ZXbZnMW7tRKprU5q'  # Change this to a random secret key