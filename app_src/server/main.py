from fastapi import FastAPI
from fastapi import FastAPI, Body, Depends
from bson import ObjectId
import random
from pymongo import UpdateOne
from fastapi.encoders import jsonable_encoder
from database import *
from bulk_items import *
from models.item import PostSchema, UserSchema, UserLoginSchema, Updated_Item, ResponseModel, Item, Payment_mtd, Address_mtd,Quanity
from auth.jwt_bearer import JWTBearer
from auth.jwt_handler import signJWT
from routes.item import router 
app = FastAPI()

users= []

app.include_router(router, tags=["Item"], prefix="/item")

@app.post("/user/signup", tags=["User Signup"])
def user_signup(user:UserSchema =Body(...)):
    users.append(user) 
    return signJWT(user.email)

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False

@app.post("/user/login", tags=["User Login"])
def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }


# @app.get("/",dependencies=[Depends(JWTBearer())], tags=["Root"])
# async def read_root():
#     return {"message": "Welcome to this fantastic app!"}

@app.put("/bulk_entries",response_description="Item buy from the database",tags=["Bulk Entries"])
async def bulk_entry():
    updates = []
    a = item_collection.insert_many([{"item_name": i, "price": j, "qty":k} for (i,j,k) in zip(names,prices,quantity)])
    updates.append(a)
    return "Item updates"


@app.post("/Adding_many_product", tags=["Cart"])
async def insert_items():
    mylist = (
  {"item_name": "Fruits", "price": 10, "qty":10},
  {"item_name": "vegetables", "price": 50, "qty":20},
  {"item_name": "Spices", "price": 15, "qty":40},
  {"item_name": "Meat", "price": 70, "qty":50},
)
    new_item = await item_collection.insert_many(mylist)
    item_collection.create_index([("item_name", pymongo.ASCENDING)],unique=True)
    return "Item added successfully."
       

@app.post("/add_item_into_cart",dependencies=[Depends(JWTBearer())], response_description="Item data added into the database",tags=["Cart"])
async def add_item_data(item: Item = Body(...)):
    item = jsonable_encoder(item)
    new_item = await add_item(item)
    return ResponseModel(new_item, "Item added successfully.")


@app.get("/get_all_products", response_description="Items retrieved",tags=["Cart"])
async def get_all_items():
    items = await retrieve_items()
    if items:
        return ResponseModel(items, "Items data retrieved successfully")
    return ResponseModel(items, "Empty list returned")


@app.get("/get_items_using_id/{id}", response_description="item data retrieved",tags=["Cart"])
async def get_item(id):
    item = await retrieve_item(id)
    if item:
        return ResponseModel(item, "item data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Item doesn't exist.")


@app.get("/get_items_using_item_name/{name}", response_description="item data retrieved",tags=["Cart"])
async def get_items_using_item_name(name:str):
    items = []
    async for item in item_collection.find({"item_name":name}):
        items.append(item_helper(item))
    return items


@app.put("/update_items_using_id/{id}",response_description="Item data update from the database",tags=["Cart"])
async def update_data(id: str, req:Item = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_item = await update_item(id, req)
    if updated_item:
        return ResponseModel(
            "Item with ID: {} name update is successful".format(id),
            "Item name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the item data.",
    )


@app.delete("/delete_items_in_cart_using_id/{id}", response_description="Item data deleted from the database",tags=["Cart"])
async def delete_item(id: str):
    deleted_item = await delete_item(id)
    if deleted_item:
        return ResponseModel(
            "Item with ID: {} removed".format(id), "Item deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Item with id {0} doesn't exist".format(id)
    )

# -------------------------------------------------------------

# Payment methods
@app.post("/Adding_payment",tags=["Payments"])
async def inserting_items():
    sample = (
  {"payment_methods": "credit_card", "transaction_id": "23XXXUH", "card_no": "23113312XXXTD","card_status": "Active","cvv": "321"},
 {"payment_methods": "cash", "transaction_id": "21XXXTD","card_no": "23122112XXXTD"},
{"payment_methods": "debit_card", "transaction_id": "7512XOTD", "card_no": "2312213312XTD","card_status": "Active","cvv": "951"},

)
    new_item = await items_collections.insert_many(sample)
    # item_collection.create_index([("payment_methods", pymongo.ASCENDING)],unique=True)
    return "Payment added successfully."

# adding payments manually
@app.post("/payments",dependencies=[Depends(JWTBearer())],response_description="payments",tags=["Payments"])
async def add_data(item: Payment_mtd = Body(...)):
    item = jsonable_encoder(item)
    new_item = await addd_items(item)
    return ResponseModel(new_item, "Payment added successfully.")


# Address methods
@app.post("/Adding_address", tags=["Address"])
async def inserting_items():
    test = (
  {"customer_name":"Arun","address":"Electronic City", "city":"Bangalore","region": "Bangalore south","country":"India","pincode":560100},
 {"customer_name":"Chandra","address":"Silicon valley", "city":"Bangalore","region": "Bangalore north","country":"India","pincode":560096},
{"customer_name":"Karti","address":"Avenue Road", "city":"Bangalore","region": "Bangalore Central","country":"India","pincode":560101},

)
    new_item = await itemss_collections.insert_many(test)
    # item_collection.create_index([("payment_methods", pymongo.ASCENDING)],unique=True)
    return "Address added successfully."

# adding address manually
@app.post("/address",dependencies=[Depends(JWTBearer())],response_description="payments",tags=["Address"])
async def add_data(item: Address_mtd = Body(...)):
    item = jsonable_encoder(item)
    new_item = await adddd_items(item)
    return ResponseModel(new_item, "Item added successfully.")
 


 # Buying the items
@app.put("/buying_items_using_id/{id}",response_description="Item buy from the database",tags=["Item Buy"])
async def Item_buy(id: str,pyt_id,addr_id, req:Quanity = Body(...)):
    qty = {k: v for k, v in req.dict().items() if v is not None}
    updated_item = await update_item(id,qty)
    # item = await retrieve_item(id
    items = []
    item = await retrieve_item(id)
    a = item.get("qty")
    b = item.get("price")
    Total_val = a * b 
    item = await retrievesss_items(pyt_id)
    items.append(item)
    item = await retrievessss_items(addr_id)
    items.append(item)

    await item_collection.delete_one({"_id": ObjectId(id)})
    # await item_collections.delete_one({"_id": ObjectId(itm_id)})
    
    if Total_val:
        return (
            "Total quantity you bought is {},the total amount is {b}".format(a,b=Total_val),
            items,
            "Item Brought Successfully",
        )

    
@app.get("/find_items_between_range",response_description="Item buy from the database",tags=["Find Items Between the Range"])
async def find_item(a:int,b:int):
    count = 0
    items = []
    async for item in item_collection.find({"qty":{"$gt":a, "$lt":b}}):   
        '''For getting item info by giving the qty b/w the range'''
    # async for item in item_collection.find({"qty":{"$gt":a, "$lt":b}}):  
    #      '''For getting item info by giving the price b/w the range'''
        items.append(item_helper(item))
        count = count + 1
    return ["Total count of the items is : ",count,items]


@app.get("/find_objectId_in_range",response_description="Item buy from the database",tags=["Find Items ID in the range"])
async def find_item(a:int):
    count = 0
    items = []
    async for item in item_collection.find({"_id":{"$gt":ObjectId("62a6cbaf9ca6061a209d3614")}}).limit(a):
        items.append(item_helper(item))
        count = count + 1
    return count,items
       
    

    