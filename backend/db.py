import time
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# set in docker-compose.yml
DATABASE_URL = os.getenv("DATABASE_URL")

# retry logic for connecting to the database
# MySQL database container was sometimes still initializing when the backend container tried to connect, which caused a connection failure
engine = None
for attempt in range(10):
    try:
        # SQLAlchemy engine (echo=True logs SQL queries)
        engine = create_engine(DATABASE_URL, echo=True)
        # test connection to ensure the database is ready
        connection = engine.connect()
        connection.close()
        break
    except OperationalError:
        time.sleep(5)
else:
    raise Exception("Database not reachable. Check connection settings.")

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
