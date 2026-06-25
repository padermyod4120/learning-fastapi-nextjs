from fastapi import FastAPI, HTTPException
from contextlib import contextmanager
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    String,
    insert,
    select,
    update,
    delete
)
from dotenv import load_dotenv
import os
load_dotenv()

# Database
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Database URL: {DATABASE_URL}")
engine = create_engine(DATABASE_URL, echo=False, future=True)
metadata = MetaData()

# Table
tb_book = Table(
    "tb_book",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("price", Float, nullable=False),
)

metadata.create_all(engine)

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


app = FastAPI()

@app.get('/books')
def list_books():
    with get_connection() as conn:
        result = conn.execute(select(tb_book).order_by(tb_book.c.id)).all()
        print(f"Result: {result}")
        return [dict(row._mapping) for row in result]

@app.get('/books/{book_id}')
def get_book(book_id: int):
    with get_connection() as conn:
        result = conn.execute(select(tb_book).where(tb_book.c.id == book_id)).first()

        if not result:
            raise HTTPException(status_code=404, detail="Book not found")

        return dict(result._mapping)
    
@app.post('/books')
def create_book(book: dict):
    with get_connection() as conn:
        conn.execute(insert(tb_book).values(book))
        return {"message": "Book created successfully"}

@app.put('/books/{book_id}')
def update_book(book_id: int, book: dict):
    with get_connection() as conn:
        conn.execute(update(tb_book).where(tb_book.c.id == book_id).values(book))
        return {"message": "Book updated successfully"}
    
@app.delete('/books/{book_id}')
def delete_book(book_id: int):
    with get_connection() as conn:
        conn.execute(delete(tb_book).where(tb_book.c.id == book_id))
        return {"message": "Book deleted successfully"}