from sqlalchemy import Column, DateTime, Integer, String, text
from database import Base, engine

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(70), unique=True, nullable=False)
    date_created = Column(DateTime, server_default=('NOW()'))
    date_updated = Column(DateTime, server_onupdate=('NOW()'))
    deleted = Column(Integer, default=0)

try:
    Base.metadata.create_all(engine)
except:
    print("Model already created on database")
