from fastapi import FastAPI
from auth_routes import auth_router 
from order_routes import order_router
import uvicorn


app = FastAPI() 


app.include_router(auth_router)
app.include_router(order_router)


if __name__ == '__main__': 
    uvicorn.run("main:app", host='127.0.0.1', port=5000, reload=True)