from pathlib import Path
import csv
from datetime import datetime

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"

FILES = {
    "students.csv": ["id","name","email","department","password"],
    "admins.csv": ["id","username","password","name"],
    "menu.csv": ["id","name","category","price","availability"],
    "orders.csv": ["order_id","student_id","student_name","items","total","status","date"]
}

def ensure_data_files():
    DATA.mkdir(exist_ok=True)
    defaults = {
        "admins.csv": [
            {"id":"A001","username":"admin","password":"admin123","name":"CampusBite Admin"}
        ],
        "menu.csv": [
            {"id":"F001","name":"Vada Pav","category":"Snacks","price":"20","availability":"Yes"},
            {"id":"F002","name":"Samosa","category":"Snacks","price":"15","availability":"Yes"},
            {"id":"F003","name":"Masala Dosa","category":"South Indian","price":"60","availability":"Yes"},
            {"id":"F004","name":"Veg Sandwich","category":"Fast Food","price":"50","availability":"Yes"},
            {"id":"F005","name":"Veg Burger","category":"Fast Food","price":"70","availability":"Yes"},
            {"id":"F006","name":"Cheese Pizza","category":"Fast Food","price":"120","availability":"Yes"},
            {"id":"F007","name":"French Fries","category":"Sides","price":"55","availability":"Yes"},
            {"id":"F008","name":"Cold Coffee","category":"Beverages","price":"50","availability":"Yes"},
            {"id":"F009","name":"Lemon Juice","category":"Beverages","price":"30","availability":"Yes"},
            {"id":"F010","name":"Chocolate Brownie","category":"Dessert","price":"45","availability":"Yes"},
        ],
    }
    for filename, headers in FILES.items():
        path = DATA / filename
        if not path.exists():
            with open(path,"w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=headers); w.writeheader()
                for row in defaults.get(filename,[]): w.writerow(row)

def read_csv(filename):
    ensure_data_files()
    with open(DATA/filename,newline="",encoding="utf-8") as f:
        return list(csv.DictReader(f))

def write_csv(filename, rows):
    headers = FILES[filename]
    with open(DATA/filename,"w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=headers); w.writeheader(); w.writerows(rows)

def append_row(filename,row):
    headers=FILES[filename]
    with open(DATA/filename,"a",newline="",encoding="utf-8") as f:
        csv.DictWriter(f,fieldnames=headers).writerow(row)

def find_row(filename,key,value):
    return next((r for r in read_csv(filename) if r.get(key)==value),None)

def next_id(filename,key,prefix=""):
    rows=read_csv(filename)
    nums=[]
    for r in rows:
        v=r.get(key,"")
        try: nums.append(int(v.replace(prefix,"")))
        except: pass
    return f"{max(nums,default=0)+1:03d}"

def money(v):
    return f"₹{float(v):,.2f}"

def timestamp():
    return datetime.now().strftime("%d-%m-%Y %I:%M %p")
