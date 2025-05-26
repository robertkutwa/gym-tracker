# gym_tracker/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define Base without importing models
Base = declarative_base()

# Set up engine and session
engine = create_engine('sqlite:///gym.db')
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)