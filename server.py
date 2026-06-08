from fastapi import FastAPI, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.post("/upload/")
async def upload_file(my_file: UploadFile = File(...)):
    dir = "uploads"
    if not os.path.exists(dir):
        os.makedirs(dir)
    file_path = os.path.join(dir, my_file.filename)
    with open(file_path, "wb") as f:
        f.write(my_file.file.read())
    return {"filename": my_file.filename, "file_path": file_path}

@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}!"}

@app.get("/search")
async def search(name: str, age: int):
    return {"message": f"Searching for {name} and {age} years old."}

#post

customers = []

@app.post("/items")
async def create_item(customer: dict):
    customers.append(customer)
    return {"message": "Customer added successfully", "customer": customers}

@app.put('/customer/{customer_id}')
async def update_customer(customer_id: int, customer: dict):
    return {"customer_id": customer_id, "customer": customer}

@app.delete('/customer/{customer_id}')
async def delete_customer(customer_id: int):
    return {'customer_id': customer_id}


@app.get("/env_values")
async def get_env_value():
    secret_key = os.getenv("SECRET_KEY")
    return {"SECRET_KEY": secret_key}