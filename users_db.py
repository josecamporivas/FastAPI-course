from fastapi import FastAPI, HTTPException, status
from db.models.user import User
from db.schemas.user import user_schema, users_schema
from db.client import db_client

from bson import ObjectId

app = FastAPI()


@app.get("/userdb", response_model=list[User])
async def get_users():
    return users_schema(db_client.users.find())

@app.get("/userdb/{user_id}")
async def get_user(user_id: str):
    return search_user('_id', ObjectId(user_id))

# post method
@app.post("/userdb", response_model=User, status_code=status.HTTP_201_CREATED)
async def post_user(user: User):
    if type(search_user('email',user.email)) == User:
        raise HTTPException(status_code=404, detail="Ya existe un usuario con ese email")

    user_dict = dict(user)
    del user_dict["id"]

    id = db_client.users.insert_one(user_dict).inserted_id
    
    inserted_user = user_schema(db_client.users.find_one({"_id": id}))

    return User(**inserted_user)

# put method
@app.put("/userdb", response_model=User)
async def modify_user(user: User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        db_client.users.find_one_and_replace({'_id': ObjectId(user.id)}, user_dict)
    except:
        return {"error": "No existe ese usuario"}
        
    return search_user('_id', ObjectId(user.id))

# delete method
@app.delete("/userdb/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def get_user(user_id: str):
    found = db_client.users.find_one_and_delete({'_id':ObjectId(user_id)})
    
    if not found:
        return {"error": "No existe ese usuario"}

def search_user(field:str, value):
    try:
        user = user_schema(db_client.users.find_one({field: value}))
        return User(**user)
    except:
        return {'error': 'El usuario no se ha encontrado'}
