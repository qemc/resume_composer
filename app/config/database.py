from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from functools import wraps

load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def with_session_query(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with SessionLocal() as session:
            return func(session, *args, **kwargs)
    return wrapper

def with_session_edit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with SessionLocal() as session:
            try:
                result = func(session, *args, **kwargs) # here is a moment where wapping function is placed. 
                session.commit()
                return result
            except Exception as e:
                session.rollback()
                raise e
    return wrapper