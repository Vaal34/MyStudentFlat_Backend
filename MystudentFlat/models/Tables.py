from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, create_engine, DateTime, Index
from sqlalchemy.orm import relationship, declarative_base, Mapped
from sqlalchemy.orm import mapped_column


Base = declarative_base()

class Appartment(Base):
    __tablename__ = 'appartment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    price = Column(Integer)
    ref = Column(String(20))
    description = Column(Text)
    square_meter = Column(Float)
    address = Column(String(255))
    postal_code = Column(Integer)
    url = Column(String(255))
    agency = Column(String(255))
    phonenumber = Column(String(20))
    created_at = Column(DateTime)
    picture_table = relationship("Pictures", back_populates="appart_table", cascade="all, delete")

class Pictures(Base):
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True)
    flat_id = Column(Integer, ForeignKey("appartment.id"))
    URL_picture = Column(Text)
    appart_table = relationship("Appartment", back_populates="picture_table")
