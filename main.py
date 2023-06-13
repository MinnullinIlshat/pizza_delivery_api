from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from auth_routes import auth_router 
from order_routes import order_router
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from schemas import Settings
import uvicorn


app = FastAPI() 

@AuthJWT.load_config
def get_config():
    return Settings()

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

app.include_router(auth_router)
app.include_router(order_router)



if __name__ == '__main__': 
    uvicorn.run("main:app", host='127.0.0.1', port=5000, reload=True)