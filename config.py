import os
from dotenv import load_dotenv
# Load .env file (only for local dev)
load_dotenv()

ENV = os.getenv("flask_env", "development").lower()

if ENV == "production":
    DB_PATH = os.getenv("DATABASE_PATH", "salary.db")
    CSV_PATH_TEXT = os.getenv("CSV_PATH_TEXT", "salary_live")
else:
    DB_PATH = os.getenv("DATABASE_LOCAL_PATH", "salary_local.db")
    CSV_PATH_TEXT = os.getenv("CSV_LOCAL_PATH_TEXT", "salary_local")

