# db.py
import os
import urllib.parse
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Get and encode password
db_password = os.getenv("PASSWORD")
safe_password = urllib.parse.quote_plus(db_password)

# Construct database URL
SUPABASE_DB_URL = (
    f"postgresql://postgres:{safe_password}@db.zceyswtlmkcrvzgoiyuw.supabase.co:5432/postgres"
)

# Create SQLAlchemy engine
engine = create_engine(SUPABASE_DB_URL)

# Function to get connection (return Engine, not open Connection)
def get_connection():
    return engine
