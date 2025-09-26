import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./attendance_system.db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production-make-it-long-and-random")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
