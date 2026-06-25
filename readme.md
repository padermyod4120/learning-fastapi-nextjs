# run server
uvicron server:app --reload

# before migrate
alembic revision --autogenerate -m "add remark column"

# migrate
alembic upgrade head