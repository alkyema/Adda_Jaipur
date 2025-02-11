from fastapi import FastAPI, Request, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List, Optional

from user import refresh
from Get_Inventory_Item import retrieve_all_data,retrieve_dict_data,filter

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.get("/")
# def read_root():
#     return "hello it is working"

@app.get("/cameranotification")
def read_root():
    return refresh()

@app.get("/default")
def default():
    return "hello it is working"

@app.get("/All_Data")
def All_Data():
    return retrieve_all_data()

@app.get("/Dict_Data")
def Dict_Data():
    return retrieve_dict_data()

class filterClass(BaseModel):
    category: Optional[List[str]] = []
    subcategory: Optional[List[str]] = []
    price: Optional[List[float]] = []
    size: Optional[List[str]] = []
    color: Optional[List[str]] = []

@app.post("/filterAPI")
def filterFunction(filterClass: filterClass, request: Request):
    
    print(filterClass.category,filterClass.subcategory,filterClass.price,filterClass.size,filterClass.color)
    return filter(filterClass.category,filterClass.subcategory,filterClass.price,filterClass.size,filterClass.color)