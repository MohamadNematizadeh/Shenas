from pymongo import MongoClient
from fastapi import FastAPI
from .tasks import add_numbers

app = FastAPI()

client = MongoClient("mongodb://mongodb:27017/")
db = client.ekyc_db

@app.get("/add-sample/")
def add_sample():
    db.users.insert_one({"name": "John Doe"})
    return {"message": "User added"}

@app.get("/add/")
def add_numbers_route(a: int, b: int):
    task = add_numbers.delay(a, b)
    return {"task_id": task.id}
