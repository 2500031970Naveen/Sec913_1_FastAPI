# pip install fastapi uvicorn pydantic sqlalchemy psycopg2
# uvicorn userauth:app --reload

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String  
from sqlalchemy.orm import sessionmaker, declarative_base

# ================= DATABASE =================
DATABASE_URL = "postgresql://postgres:admin123@localhost:5432/TaskHub"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ================= MODEL =================
class User(Base):
    __tablename__ = "users"   # ✅ FIXED
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Integer)
    pending_task = Column(Integer)

# Create table (skip on startup - will create on first API call if needed)
# Base.metadata.create_all(bind=engine)

# ================= FASTAPI =================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= REQUEST MODELS =================
class LoginRequest(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str
    role: int
    pending_task: int

# ================= ROUTES =================

@app.get("/products")
def get_products():
    return [
        {"name": "Laptop", "price": 70000},
        {"name": "Mobile", "price": 20000},
        {"name": "Projector", "price": 22222},
        {"name": "Tablet", "price": 30000}
    ]

@app.get("/welcome")
def welcome():
    return "Welcome to Sec913 New"

# ================= LOGIN =================
@app.post("/login")
def login(data: LoginRequest):
    db = SessionLocal()
    
    user = db.query(User).filter(
        User.username == data.username,
        User.password == data.password
    ).first()
    
    db.close()

    if user:
        return {
            "UserStatus": 1,
            "UserRole": user.role,
            "UserPendingTask": user.pending_task
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")  # ✅ FIXED

# ================= ADD USER =================
@app.post("/add_user")
def add_user(user: UserCreate):
    db = SessionLocal()

    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        password=user.password,
        role=user.role,
        pending_task=user.pending_task
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return {
        "message": "User added successfully",
        "user_id": new_user.id
    }