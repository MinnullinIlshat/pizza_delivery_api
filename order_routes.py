from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import Session, engine



order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
) 

session = Session(bind=engine)

@order_router.post('/', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, Authorize: AuthJWT=Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username==current_user).first() 
    
    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,
    )
    
    new_order.user = user
    session.add(new_order)
    session.commit()
    
    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status,
    }
    
    return jsonable_encoder(response)

@order_router.get('/all')
async def list_all_orders(Authorize: AuthJWT=Depends()): 
    Authorize.jwt_required()
        
    current_user = Authorize.get_jwt_subject()
    
    user = session.query(User).filter(User.username==current_user).first()
    if user.is_staff:
        orders = session.query(Order).all()
        
        return jsonable_encoder(orders)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not a superuser")
    
@order_router.get('/{id}')
async def get_order_by_id(id: int, Authorize: AuthJWT=Depends()):
    Authorize.jwt_required()
    
    user = Authorize.get_jwt_subject()
    
    current_user = session.query(User).filter(User.username==user).first()
    
    if current_user.is_staff:
        order = session.query(Order).filter(Order.id==id).first()
        
        return jsonable_encoder(order)
    
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User not allowed to carry out request")
    
@order_router.get('/')
async def get_user_orders(Authorize: AuthJWT=Depends()):
    Authorize.jwt_required()
        
    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username==user).first()
    return jsonable_encoder(current_user.orders)

@order_router.get('/my/{id}')
async def get_specific_order(id: int, Authorize: AuthJWT=Depends()):
    Authorize.jwt_required()
    
    user = Authorize.get_jwt_subject()
    
    current_user = session.query(User).filter(User.username==user).first()
    orders = current_user.orders
    
    for order in orders: 
        if order.id == id:
            return jsonable_encoder(order)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No order with such id")
    
@order_router.put('/{id}')
async def update_order(id: int, order: OrderModel, Authorize: AuthJWT=Depends()):
    Authorize.jwt_required()
        
    update_order: OrderModel = session.query(Order).filter(Order.id==id).first()
    update_order.quantity = order.quantity
    update_order.pizza_size = order.pizza_size
    
    session.commit()
    
    return jsonable_encoder(update_order)

@order_router.patch('/{id}')
async def update_order_status(id: int, 
                              order: OrderStatusModel,
                              Authorize: AuthJWT=Depends()):
    Authorize.jwt_required()
        
    user = Authorize.get_jwt_subject()
    
    current_user = session.query(User).filter(User.username==user).first()
    
    if current_user.is_staff: 
        update_order: OrderModel = session.query(Order).filter(Order.id==id).first()
        update_order.order_status = order.order_status
        
        session.commit()
        
        response = {
            "id": update_order.id,
            "quantity": update_order.quantity,
            "pizza_size": update_order.pizza_size,
            "order_status": update_order.order_status
        }
        
        return jsonable_encoder(response)
    
@order_router.delete('/{id}',
                     status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id: int, Authorize: AuthJWT=Depends()):
    Authorize.jwt_required()
        
    del_order = session.query(Order).filter(Order.id==id).first()
    
    session.delete(del_order)
    session.commit()
    
    return del_order