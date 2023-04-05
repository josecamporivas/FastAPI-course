from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 

from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = 'HS256'
ACCESS_TOKEN_DURATION = 1
SECRET = '201d573bd7d1344d3a3bfce1550b69102fd11be3db6d379508b6cccc58ea230b' # to generate this code I use: openssl rand -hex 32 

crypt = CryptContext(schemes=['bcrypt'])

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "josecampo": {
        "username": "josecampo",
        "full_name": "Jose Campo",
        "email": "jose@gmail.com",
        "disabled": False,
        "password": "$2a$12$9UYiYfk1K6aMqUeoTh0l1.4SX.95OGXCmYIG4EWVlVD5BHAC0/IAO"

    },
    "josecampo2": {
        "username": "josecampo2",
        "full_name": "Jose2 Campo2",
        "email": "jose2@gmail.com",
        "disabled": True,
        "password": "$2a$12$18aW7THCuFTA5UaXQKUa4.FtuJWZ55ug78w6j0IiSvtkF15tZw32."

    }
}

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

async def auth_server(token: str = Depends(oauth2)):

    exception_401 = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autenticación inválidas",
            headers={'WWW-Authenticate': 'Bearer'})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
    except JWTError:
        raise exception_401
    
    if username is None:
        raise exception_401
    
    user = search_user(username)
    if not user:
        raise exception_401
    
    return user

async def current_user(user: User = Depends(auth_server)):
    if user.disabled:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo")

    return user


@app.post('/login')
async def login(form : OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El usuario no es correcto")
    
    user = search_user_db(form.username)

    passwordVerified = crypt.verify(form.password, user.password)

    if not passwordVerified:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La contraseña no es correcta")
    
    access_token_expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)

    access_token = {
        "sub": user.username,
        "exp": access_token_expiration
    }

    return {
        "access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM),
        "token_type": "bearer"
    }

@app.get('/users/me')
async def me(user: User = Depends(current_user)):
    return user