from fastapi import FastAPI, HTTPException, Request, Response
from pydantic import BaseModel
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Database connection
db_client = AsyncIOMotorClient('mongodb://localhost:27017')
db = db_client['book_shopping']
user = 'user'
passcode = 'pass'

# Models
class books(BaseModel):
    product_id: str
    name: str
    author: str
    pages: int 
    genres: List[str]
    price: float
    stock: int

class Order(BaseModel):
    product_id: str
    quantity: int
    account: str

#  set for queried products
queried_products = set()

# Routes
@app.get("/")
async def root():
    return {"message": "Welcome to the Bookstore "}


@app.get("/products/{product_id}")
async def get_product(product_id: str):
    product = await db['books'].find_one({"product_id": product_id})
    if product:
        product["_id"] = str(product["_id"])  # Convert ObjectId to string
        queried_products.add(product_id)  # Add product_id to set
        return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/orders/", status_code=201)
async def place_order(order: Order, request: Request):
    # Authenticate user
    username = request.headers.get('Username')
    password = request.headers.get('Password')
    if not (username ==user and password ==passcode):
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Check if product has been queried
    if order.product_id not in queried_products:
        raise HTTPException(status_code=400, detail="Product must be queried before ordering")

    # Check if product exists
    product = await db['books'].find_one({"product_id": order.product_id})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if account has sufficient credit
    account = await db['accounts'].find_one({"account_id": order.account})
    if not account or account['credit_line'] < order.quantity * product['price']:
        raise HTTPException(status_code=400, detail="Insufficient credit")

    # Place the order
    order_dict = order.dict()
    await db['orders'].insert_one(order_dict)
    return {"message": "Order placed successfully"}

