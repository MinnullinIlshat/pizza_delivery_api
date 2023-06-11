from pydantic import BaseModel, EmailStr


class SignUpModel(BaseModel):
    id: int | None
    username: str 
    email: EmailStr
    password: str
    is_staff: bool | None
    is_active: bool | None
    
    class Config: 
        orm_mode=True 
        schema_extra = {
            'example':{
                "username": "johndoe",
                "email": "johndoe@gmail.com",
                "password": "password",
                "is_staff": False,
                "is_active": True,
            }
        }
        

class Settings(BaseModel):
    authjwt_secret_key: str='eb030988e7e9268822d2bfcfe454b7d78ae8c5c0f3c0638b2025028d7b0412ff'
    

class LoginModel(BaseModel):
    username: str 
    password: str 


class OrderModel(BaseModel):
    id: int | None
    quantity: int
    order_status: str = "PENDING"
    pizza_size: str = "SMALL"
    user_id: int | None
    
    class Config: 
        orm_mode = True