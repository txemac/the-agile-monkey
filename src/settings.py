import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = os.getenv("DATABASE_URL")

# Auth
SECRET_KEY = os.getenv("SECRET_KEY")
