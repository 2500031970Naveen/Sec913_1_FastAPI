from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/products")
def read_root():
    return [
        {"name": "Laptop", "price": 70000},
        {"name": "Mobile", "price": 20000},
        {"name": "Tablet", "price": 30000}
    ]
    
    
    
    

