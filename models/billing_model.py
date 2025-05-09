from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base, engine
from sqlalchemy.sql import func

class Billing(Base):
    __tablename__ = "tbl_billings"
    id = Column(Integer, primary_key=True, index=True)
    remarks = Column(String(200), nullable=True)
    billing_date = Column(DateTime, nullable = False)
    amount = Column(Float, nullable = False)
    date_created = Column(DateTime, server_default=func.now())
    date_updated = Column(DateTime, server_onupdate=func.now())
    deleted = Column(Integer, default = 0)

    user_id = Column(Integer, ForeignKey('tbl_users.id'), nullable = False)
    category_id = Column(Integer, ForeignKey('tbl_categories.id'), nullable = False)

    user_billing = relationship("User", foreign_keys=[user_id])
    category_billing = relationship("Category", foreign_keys=[category_id])
try:
    Base.metadata.create_all(engine)
except Exception as error:
    print("Model already created on database")
    print(error)

