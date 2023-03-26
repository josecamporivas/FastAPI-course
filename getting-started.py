from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    age: int


users_db = [User(id=0,name="Jose", age=21),
    User(id=1,name="Antonio", age=19),
    User(id=2,name="Carlos", age=70),
    User(id=3,name="Alberto", age=56),
    User(id=4,name="Maria", age=34),
    User(id=5,name="Josefina", age=29)]

# root path
@app.get("/")
async def root():
    return {"message": "Hello World"}

# path parameters
# example URL: http://localhost:8000/users/5
@app.get("/user/{user_id}")
async def get_user(user_id: int):
    try:
        user = search_user(user_id)[0]
    except:
        return {"error": "No existe un usuario con ese id"}
    
    return {"item_id": user_id, "user": user}

# query parameters
# example URL: http://localhost:8000/users/?max_age=30
@app.get("/users/")
async def filter_age_users(max_age: int = 50):
    users_filtered = list(filter(lambda user: user.age < max_age, users_db))
    return {"max_age": max_age, "user": users_filtered}

# post method
@app.post("/user/")
async def post_user(user: User):
    if len(search_user(user.id) == 0):
        users_db.append(user)
        return user
    else:
        return {"error": "Ya existe un usuario con ese id"}

# put method
@app.put("/user/")
async def modify_user(user: User):
    found = False
    for index,user_db in enumerate(users_db):
        if user_db.id == user.id:
            users_db[index] = user
            found = True
    
    if not found:
        return {"error": "No existe ese usuario"}
    
    return user

# delete method
@app.delete("/user/{user_id}")
async def get_user(user_id: int):
    found = False
    for index,user_db in enumerate(users_db):
        if user_db.id == user_id:
            del users_db[index]
            found = True
    
    if not found:
        return {"error": "No existe ese usuario"}

def search_user(id: int):
    return list(filter(lambda user: user.id == id, users_db))