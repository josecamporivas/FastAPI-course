from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix='/products', tags=["product"])

class Product(BaseModel):
    id: int
    name: str
    price: int

products_db = [
    Product(id=0, name="Bread",price=1),
    Product(id=1, name="Pizza",price=43),
    Product(id=2, name="Apple",price=6),
    Product(id=3, name="Laptop",price=69),
    Product(id=4, name="Water",price=51)
]

@router.get('/')
async def products():
    return products_db

@router.get('/{id}')
async def products(id : int):
    if(id < 0 or id >= len(products_db)):
        raise HTTPException(status_code=404, detail="Id not valid")

    return products_db[id]