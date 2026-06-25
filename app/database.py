from sqlalchemy import create_engine, MetaData
from contextlib import contextmanager
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=False, future=True)
metadata = MetaData()

@contextmanager
def get_connection():
    conn = engine.connect()
    trans = conn.begin()
    try:
        yield conn
        trans.commit()
    except Exception as e:
        trans.rollback()
    finally:
        conn.close()