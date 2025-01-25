from collections import OrderedDict
from firebase_admin import db
# import Connect_Firebase
import datetime
import re

# Reference to your Firebase Realtime Database
data = {}
collection = {}
product = []
dict_prod = {}

ref = db.reference('Inventory')
data = ref.get()


collection = {key: list(value.keys()) for key, value in data.items()}

def refresh():
    """
    Refresh the global product list by iterating over the database structure.
    """
    product.clear()
    for category in collection:
        for subcategory in collection[category]:
            try:
                # Single product case
                if (data[category][subcategory]['ProductID']):
                    data[category][subcategory]['Category'] = category
                    data[category][subcategory]['Name'] = subcategory
                    product.append(data[category][subcategory])
            except:
                # Multiple products case
                for k in data[category][subcategory]:
                    data[category][subcategory][k]['Category'] = category
                    data[category][subcategory][k]['Sub_Category'] = subcategory
                    data[category][subcategory][k]['Name'] = k
                    product.append(data[category][subcategory][k])
                continue
            
def dict_refresh():
    """
    Refresh the global dictionary of products indexed by ProductID.
    """
    dict_prod.clear()
    for category in collection:
        for subcategory in collection[category]:
            try:
                # Single product case
                if (data[category][subcategory]['ProductID']):
                    data[category][subcategory]['Category'] = category
                    data[category][subcategory]['Name'] = subcategory
                    dict_prod[f"ProductID{data[category][subcategory]['ProductID']}"] = data[category][subcategory]
            except:
                # Multiple products case
                for k in data[category][subcategory]:
                    data[category][subcategory][k]['Category'] = category
                    data[category][subcategory][k]['Sub_Category'] = subcategory
                    data[category][subcategory][k]['Name'] = k
                    dict_prod[f"ProductID{data[category][subcategory][k]['ProductID']}"] = data[category][subcategory][k]
                continue



def retrieve_all_data():
    """
    Retrieve all product data as a list.
    """
    refresh()
    return product

def retrieve_dict_data():
    """
    Retrieve all product data as a dictionary indexed by ProductID.
    """
    dict_refresh()
    return dict_prod

def filter(category=list, subcategory=list, price=int, size=list, color=list):
    return_List = []
    working_list = []

    if(category != []):
        for PD_category in product:
            if(PD_category['Category'] in category):
                working_list.append(PD_category)
        if working_list == []:
            return []
    
    return_List = working_list.copy()
    
    if(return_List == []):
        working_list.clear()
        if(subcategory != []):
            for PD_subcategory in product:
                try:
                    if(PD_subcategory['Sub_Category'] in subcategory):
                        working_list.append(PD_subcategory)
                except:
                    continue
            if working_list == []:
                return []
    else:
        if(subcategory != []):
            working_list.clear()
            for PD_subcategory in return_List:
                try:
                    if(PD_subcategory['Sub_Category'] in subcategory):
                        working_list.append(PD_subcategory)
                except:
                    continue
            if working_list == []:
                return []
    
    return_List = working_list.copy()
    
    if(return_List == []):
        working_list.clear()
        if(size != []):
            for PD_subcategory in product:
                try:
                    common = common = [item for item in PD_subcategory["Size"] if item in size]
                    if common:                        
                        working_list.append(PD_subcategory)
                except:
                    continue
            if working_list == []:
                return []
    else:
        if(size != []):
            working_list.clear()
            for PD_subcategory in return_List:
                try:
                    common = common = [item for item in PD_subcategory["Size"] if item in size]
                    if common:
                        working_list.append(PD_subcategory)
                except:
                    continue
            if working_list == []:
                return []
    
    return_List = working_list.copy()
    
    if(return_List == []):
        working_list.clear()
        if(color != []):
            for PD_subcategory in product:
                try:
                    if(PD_subcategory['Color'] in color):
                        working_list.append(PD_subcategory)
                except:
                    continue
            if working_list == []:
                return []
    else:
        if(color != []):
            working_list.clear()
            for PD_subcategory in return_List:
                try:
                    if(PD_subcategory['Color'] in color):
                        working_list.append(PD_subcategory)
                except:
                    continue
            if working_list == []:
                return []
    
    return_List = working_list.copy()
    if(return_List == []):
        working_list.clear()
        if(price != []):
            for PD_subcategory in product:
                try:
                    if(PD_subcategory['Price'] >= price[0] and PD_subcategory['Price'] <= price[1]):
                        working_list.append(PD_subcategory)
                except:
                    continue
            if working_list == []:
                return []
    else:
        if(price != []):
            working_list.clear()
            for PD_subcategory in return_List:
                try:
                    if(PD_subcategory['Price'] >= price[0] and PD_subcategory['Price'] <= price[1]):
                        # print("called")
                        working_list.append(PD_subcategory)
                except:
                    continue
            if working_list == []:
                return []
    
    return_List = working_list.copy()
    
    return return_List
    

if __name__ == "__main__":
    refresh()
    print(filter(category=[], subcategory=[], price=[3000,4000], size=[], color=[]))
