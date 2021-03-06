from sqlalchemy import Integer, String, Column, Date
from sqlalchemy.orm import relationship

from db.base import Base
from .order_medicine_association import order_medicine


# create database "tbl_medicines"
class Medicines(Base):
    __tablename__ = "tbl_medicines"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), unique=True)
    slug = Column(String(50))
    medical_function = Column(String(50))
    quantity = Column(Integer)
    price = Column(String(30))
    manufacture_date = Column(Date)
    expire_date = Column(Date)
    status = Column(String(20), nullable=False)
    orders = relationship(
        "Orders", secondary=order_medicine, back_populates="medicines"
    )
