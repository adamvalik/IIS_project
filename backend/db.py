from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# set in docker-compose.yml
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy engine (echo=True logs SQL queries)
engine = create_engine(DATABASE_URL, echo=True)

# SessionLocal class for managing sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for models
Base = declarative_base()

# dependency to get a database session
def get_db():
  db = SessionLocal()
  try:
      yield db
  finally:
      db.close()
