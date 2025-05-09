from sqlalchemy import Column, String, Integer, DateTime, text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base, engine


class Billing(Base):
    __tablename__ = "billings"
    id = Column(Integer, primary_key=True, index=True)
    remarks = Column(String(200), nullable=True)
    date = Column(DateTime, server_default=text('NOW()'))
    date_created = Column(DateTime, server_default=text('NOW()'))
    date_updated = Column(DateTime, server_onupdate=text('NOW()'))
    deleted = Column(Integer, default = 0)

    user_id = Column(Integer, ForeignKey('users.id'), nullable = False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable = False)

    user_billing = relationship("User", foreign_keys=[user_id])
    category_billing = relationship("Category", foreign_keys=[category_id])
try:
    Base.metadata.create_all(engine)
except:
    print("Model already created on database")

