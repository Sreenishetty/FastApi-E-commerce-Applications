import motor.motor_asyncio
from decouple import config
from bson import ObjectId
import pymongo

MONGO_DETAILS = config("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.items

item_collection = database.get_collection("Cart1")
item_collections = database.get_collection("Cart2")
items_collections = database.get_collection("Payments")
itemss_collections = database.get_collection("Address")

# helper
def item_helper(item) -> dict:
    return {
        "item_name": str(item["item_name"]),
        "price": item["price"],
        "qty": item["qty"]
    }

# helper
def payment_helper(item) -> dict:
    return {
        "payment_methods":str(item["payment_methods"]),
        "transaction_id":str(item["transaction_id"]),
        # "available_amount": item["available_amount"],

    }

def address_helper(item) -> dict:
    return {
            "customer_name": str(item["customer_name"]),
            "address":str(item["address"]),
            "city":str(item["city"]),
            "region": str(item["region"]),
            "country":str(item["country"]),
            "pincode":item["pincode"]
    }
# Database CRUD Operations

# Retrieve all items present in the database
async def retrieve_items():
    items = []
    async for item in item_collection.find():
         items.append(item_helper(item))
    return items

# Add a new items into to the database
async def add_item(item_data: dict) -> dict:
    item = await item_collection.insert_one(item_data)
    new_item = await item_collection.find_one({"_id": item.inserted_id})
    # new_item.create_index([("item_name", pymongo.ASCENDING)],unique=True)
    return item_helper(new_item)

# Retrieve a items with a matching ID
async def retrieve_item(id: str) -> dict:
    item = await item_collection.find_one({"_id": ObjectId(id)})
    if item:
        return item_helper(item)


# Update a item with a matching ID
async def update_item(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    item = await item_collection.find_one({"_id": ObjectId(id)})
    if item:
        updated_item = await item_collection.update_one(
            {"_id": ObjectId(id)}, {"$set":data}
        )
        if updated_item:
            return True
        return False


# Delete a item from the database
async def delete_item(id: str):
    item = await item_collection.find_one({"_id": ObjectId(id)})
    if item:
        await item_collection.delete_one({"_id": ObjectId(id)})
        return True


# -------------------------------------------------------------------------------


# Retrieve all items present in the database
async def retrievees_items():
    items = []
    async for item in item_collections.find():
            items.append(item_helper(item))
    return items

# Add a new items into to the database
async def add_items(item_data: dict) -> dict:
    item = await item_collections.insert_one(item_data)
    new_item = await item_collections.find_one({"_id": item.inserted_id})
    return item_helper(new_item)


# Retrieve a items with a matching ID
async def retrieves_items(id: str) -> dict:
    item = await item_collections.find_one({"_id": ObjectId(id)})
    if item:
        return item_helper(item)

# Update a item with a matching ID
async def update_items(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    item = await item_collections.find_one({"_id": ObjectId(id)})
    if item:
        updated_item = await item_collections.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_item:
            return True
        return False

# Delete a item from the database
async def delete_items(id: str):
    item = await item_collections.find_one({"_id": ObjectId(id)})
    if item:
        await item_collections.delete_one({"_id": ObjectId(id)})
        return True

# ------------------------------------------------------------------------------------------
# Payments
async def addd_items(item_data: dict) -> dict:
    item = await items_collections.insert_one(item_data)
    new_item = await items_collections.find_one({"_id": item.inserted_id})
    return payment_helper(new_item)

async def retrievesss_items(id: str) -> dict:
    item = await items_collections.find_one({"_id": ObjectId(id)})
    if item:
        return payment_helper(item)

# address
async def adddd_items(item_data: dict) -> dict:
    item = await itemss_collections.insert_one(item_data)
    new_item = await itemss_collections.find_one({"_id": item.inserted_id})
    return address_helper(new_item)

async def retrievessss_items(id: str) -> dict:
    item = await itemss_collections.find_one({"_id": ObjectId(id)})
    if item:
        return address_helper(item)






