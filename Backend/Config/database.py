from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Define your database connection parameters
server = '38.242.223.198'
database = 'InsureFlowDB'
username = 'sa'
password = 'dataalserver'
port = '1433'

# Create a connection string
SYNC_DATABASE_URL = f"mssql+pyodbc://{username}:{password}@{server}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

# Sync (Traditional) Database Setup
engine = create_engine(SYNC_DATABASE_URL, pool_pre_ping=True)  # Avoids stale connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Shared Base for models
Base = declarative_base()

# Dependency for sync sessions (used in sync routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # Ensures session is always returned to the pool
