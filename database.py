from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


engine = create_engine('postgresql://pzdelivery:pzdelivery@localhost/pizza_delivery',
                       echo=True)

Base = declarative_base()