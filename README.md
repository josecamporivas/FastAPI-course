# FastAPI

### Instalation
`pip install "fastapi[all]"`

### Simplest file
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### Run live server from file *getting-started.py*
`uvicorn getting-started:app --reload`

### Required dependencies for JWT Auth
`pip install "python-jose[cryptography]"`
`pip install "passlib[bcrypt]"`

### Command to generate SECRET
`openssl rand -hex 32`


# MongoDB
To install MongoDB, you have to go [here](https://www.mongodb.com/docs/manual/administration/install-community/) and follow the steps.

### Run a local instance of MongoDB
```bash
mkdir data
cd ./data
mongod --dbpath .
``` 

### Requiered dependecy to connect Python and MongoDB
`pip install pymongo`