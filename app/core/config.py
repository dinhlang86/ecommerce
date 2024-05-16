import os

SECRET_KEY = os.getenv("SECRET_KEY", "Secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
