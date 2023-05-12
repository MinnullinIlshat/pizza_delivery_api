from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('postgresql+psycopg2://smilecook:smilecook@localhost/pizza_delivery',
                       echo=True)

Base = declarative_base()

Session = sessionmaker()