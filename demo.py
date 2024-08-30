from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, Numeric
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select

# Database connection settings
DATABASE_URL = "postgresql://user:password@localhost/dbname"

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

# Creating FastAPI instance
app = FastAPI()

# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/products/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: SessionLocal = next(get_db())):
    query = select(Product).where(Product.product_id == product_id)
    result = db.execute(query).fetchone()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return ProductResponse(
        product_id=result.product_id,
        name=result.name,
        description=result.description,
        price=float(result.price)
    )

# Example endpoint to handle multiple GET requests concurrently
@app.get("/products/", response_model=List[ProductResponse])
def read_products(product_ids: List[int], db: SessionLocal = next(get_db())):
    query = select(Product).where(Product.product_id.in_(product_ids))
    results = db.execute(query).fetchall()
    
    if not results:
        raise HTTPException(status_code=404, detail="Products not found")
    
    return [
        ProductResponse(
            product_id=result.product_id,
            name=result.name,
            description=result.description,
            price=float(result.price)
        ) for result in results
    ]
