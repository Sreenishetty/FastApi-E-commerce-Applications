# FastApi-E-commerce-Applications

                        """FastApi E-commerce Applications Endpoints"""
INTRODUCTION
FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

The key features that I like in FastApi are:

Fast: Very high performance, on par with NodeJS and Go (thanks to Starlette and Pydantic). One of the fastest Python frameworks available.
Fast to code: Increase the speed to develop features by about 200% to 300%.
Fewer bugs: Reduce about 40% of human (developer) induced errors. 
Easy: Designed to be easy to use and learn. Less time reading docs.
Robust: Get production-ready code. With automatic interactive documentation.
Standards-based: Based on (and fully compatible with) the open standards for APIs: OpenAPI (previously known as Swagger) and JSON Schema

The Repository contains 5 main files namely:

main.py
This file is the entry point for the application. It contains the main routes and redirects all user requested routes to their respective functions.
database.py
This file contains the neccessary methods which interact with the main.py
models.py
This file is contains the schema and the body required for the functions.
routes.py
This file contains all the methods from models.py at one place.


Endpoints
A basic E-commerce application has features such as Log in/ Register/ Cart functionalities/ Payment Functionalities/ Admin CRUD capabilities among other functionalities.

We have the following API's
    add_item,
    delete_item,
    retrieve_item,
    retrieve_items,
    update_item,

Main useage of the programm 
This python programm is to demonstrate the shopping Scenario like adding the items into the cart and modifying it as per the uses required,
adding payment methods, address of the customer and buying the items 

Install
    FastAPI
    uvicorn
    pymongo


Usage
C:\Users\srini\OneDrive\Desktop\py-mongo\mongo_fastapi\app_src\server> uvicorn main:app --reload


