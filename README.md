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

### Run live server from file *main.py*
`uvicorn main:app --reload`