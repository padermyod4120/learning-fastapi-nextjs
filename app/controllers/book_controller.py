from fastapi import HTTPException, APIRouter
from sqlalchemy import select, update, delete, insert
from models import tb_book
from database import get_connection

router = APIRouter(prefix='/books', tags=["Books"])

@router.get('/')
def list_books():
    with get_connection() as conn:
        result = conn.execute(select(tb_book).order_by(tb_book.c.id)).all()
        print(f"Result: {result}")
        return [dict(row._mapping) for row in result]

@router.get('/{book_id}')
def get_book(book_id: int):
    with get_connection() as conn:
        result = conn.execute(select(tb_book).where(tb_book.c.id == book_id)).first()

        if not result:
            raise HTTPException(status_code=404, detail="Book not found")

        return dict(result._mapping)
    
@router.post('/')
def create_book(book: dict):
    with get_connection() as conn:
        conn.execute(insert(tb_book).values(book))
        return {"message": "Book created successfully"}

@router.put('/{book_id}')
def update_book(book_id: int, book: dict):
    with get_connection() as conn:
        conn.execute(update(tb_book).where(tb_book.c.id == book_id).values(book))
        return {"message": "Book updated successfully"}
    
@router.delete('/{book_id}')
def delete_book(book_id: int):
    with get_connection() as conn:
        conn.execute(delete(tb_book).where(tb_book.c.id == book_id))
        return {"message": "Book deleted successfully"}