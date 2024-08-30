import os
from fastapi import FastAPI, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Database connection settings from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname")

# SQLAlchemy async setup
engine = create_async_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
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

# Dependency to get the async DB session
async def get_db():
    async with SessionLocal() as session:
        yield session

@app.get("/products/{product_id}", response_model=ProductResponse)
async def read_product(product_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Product).where(Product.product_id == product_id)
    result = await db.execute(query)
    product = result.scalars().first()
    
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return product

@app.get("/products/", response_model=List[ProductResponse])
async def read_products(product_ids: List[int], db: AsyncSession = Depends(get_db)):
    query = select(Product).where(Product.product_id.in_(product_ids))
    result = await db.execute(query)
    products = result.scalars().all()
    
    if not products:
        raise HTTPException(status_code=404, detail="Products not found")
    
    return products

# To run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
