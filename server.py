from fastapi import FastAPI, File, Header, UploadFile, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import jwt
import os

from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def required_token(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, 
                            detail="Invalid token", 
                            headers={"WWW-Authenticate": "Bearer"})
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get('sub') or ""
    except jwt.PyJWKError:
        raise HTTPException(status_code=401, 
                            detail="Invalid token Authentication", 
                            headers={"WWW-Authenticate": "Bearer "})

@app.get("/protected")
async def protected(user: str = Depends(required_token)):
    return {"message": f"Hello, {user}!"}

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

@app.post('/login')
async def login(data: dict):
    if data.get('username') == 'admin' and data.get('password') == '12345':
        token = jwt.encode({"sub": data['username']}, SECRET_KEY, ALGORITHM)
        return {"access_token": token}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
@app.get('/me')
async def me(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {'user': payload.get('sub')}
    except jwt.PyJWKError:
        raise HTTPException(status_code=401, detail="Invalid token")