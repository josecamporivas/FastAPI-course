from fastapi import FastAPI
from routers import products
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)

# Static files
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/")
async def root():
    return {"message": "Hello World"}