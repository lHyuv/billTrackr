from sqlalchemy import  Column, Integer, DateTime, String, Float
from database import Base, engine
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = 'tbl_users'

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(50), unique = True, nullable=False)
    password = Column(String(100), nullable = False)
    budget = Column(Float, default = 0, nullable = True)
    deleted = Column(Integer, default = 0)
    attempts = Column(Integer, default = 0)
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, server_onupdate=func.now())

try:
    Base.metadata.create_all(engine)
except Exception as error:
    print("Model already created on database")
    print(error)