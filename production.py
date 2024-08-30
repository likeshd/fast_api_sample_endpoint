import os
from fastapi import FastAPI, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, select
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Database connection settings from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Defining the Product model
class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Numeric)

# Pydantic model for the response
class ProductResponse(BaseModel):
    product_id: int
    name: str
    description: str
    price: float

    class Config:
        orm_mode = True

# Creating FastAPI instance
app = FastAPI()

# CORS Middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to restrict origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    query = select(Product).where(Product.product_id == product_id)
    result = db.execute(query).scalars().first()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return result

@app.get("/products/", response_model=List[ProductResponse])
def read_products(product_ids: List[int], db: Session = Depends(get_db)):
    query = select(Product).where(Product.product_id.in_(product_ids))
    results = db.execute(query).scalars().all()
    
    if not results:
        raise HTTPException(status_code=404, detail="Products not found")
    
    return results

# To run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
