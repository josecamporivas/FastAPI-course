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