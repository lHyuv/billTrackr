from sqlalchemy import Column, DateTime, Integer, String, text
from database import Base, engine
from sqlalchemy.sql import func

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70), unique=True, nullable=False)
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, server_onupdate=func.now())
    deleted = Column(Integer, default=0)

try:
    Base.metadata.create_all(engine)
except Exception as error:
    print("Model already created on database")
    print(error)