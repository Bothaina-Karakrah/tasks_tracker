import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SQL_DATABASE_URI = os.getenv("SQL_DATABASE_URL")