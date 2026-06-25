from sqlalchemy import Table, Column, Integer, Float, String
from database import metadata, engine

tb_book = Table(
    "tb_book",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String, nullable=False),
    Column("price", Float, nullable=False),
)

metadata.create_all(engine)