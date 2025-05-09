from sqlalchemy import  Column, Integer, DateTime, String, text
from database import Base, engine

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key = True, index = True)
    username = Column(String(50), unique = True, nullable=False)
    password = Column(String(100), nullable = False)
    deleted = Column(Integer, default = 0)
    attempts = Column(Integer, default = 0)
    date_created = Column(DateTime, server_default=text('NOW()'))
    date_updated = Column(DateTime, server_onupdate=text('NOW()'))

try:
    Base.metadata.create_all(engine)
except:
    print("Model already created on database")