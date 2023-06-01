from sqlalchemy import Column, Integer, String, Text, ForeignKey, Float, create_engine, DateTime, Index, ForeignKeyConstraint, ARRAY
from sqlalchemy.orm import relationship, declarative_base, Mapped
 

Base = declarative_base()

class Appartment(Base):
    __tablename__ = 'appartment'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    price = Column(Float)
    ref = Column(String(20))
    description = Column(Text)
    square_meter = Column(Float)
    address = Column(String(255))
    postal_code = Column(Integer)
    url = Column(String(255))
    agency = Column(String(255))
    phonenumber = Column(String(50))
    created_at = Column(DateTime)
    picture_table = relationship("Pictures", back_populates="appart_table", cascade="all, delete")
    additional_table = relationship("AdditionalSurfaces", back_populates="appart_table", cascade="all, delete")
    amenities_table = relationship("Amenities", back_populates="appart_table", cascade="all, delete")
    BuildCharac_table = relationship("BuildingCharacteristics", back_populates="appart_table", cascade="all, delete")
    Lease_rent_table = relationship("LeaseRentCharges", back_populates="appart_table", cascade="all, delete")
    PropertyCharac_table = relationship("PropertyCharacteristics", back_populates="appart_table", cascade="all, delete")

class Pictures(Base):
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True)
    flat_id = Column(Integer, ForeignKey('appartment.id', ondelete='CASCADE'))
    URL_picture = Column(Text)
    appart_table = relationship("Appartment", back_populates="picture_table")

class AdditionalSurfaces(Base):
    __tablename__ = 'additional_surfaces'

    id = Column(Integer, primary_key=True)
    flat_id = Column(Integer, ForeignKey("appartment.id", ondelete='CASCADE'))
    Cellar = Column(String(50))
    Private_parking = Column(String(50))
    appart_table = relationship("Appartment", back_populates="additional_table")

class Amenities(Base):
    __tablename__ = 'amenities'
    
    amenities_id = Column(Integer, primary_key=True)
    flat_id = Column(Integer, ForeignKey('appartment.id', ondelete='CASCADE'))
    Bathtub = Column(String(15))
    Kitchen_sink = Column(String(20))
    Washbasin = Column(String(15))
    Washing_machine_connection = Column(String(15))
    Ventilation_system = Column(String(15))
    TV_antenna = Column(String(15))
    Shower = Column(String(15))
    appart_table = relationship("Appartment", back_populates="amenities_table")

class BuildingCharacteristics(Base):
    __tablename__ = 'building_characteristics'
    
    building_charac_id = Column(Integer, primary_key=True, autoincrement=True)
    flat_id = Column(Integer, ForeignKey('appartment.id', ondelete='CASCADE'))
    Year_of_construction = Column(Integer)
    Number_of_Floor = Column(Integer)
    Digicode = Column(String(15))
    Elevator = Column(String(15))
    Green_peaces = Column(String(15))
    TV_antenna = Column(String(20))
    Cleaning_company = Column(String(20))

    appart_table = relationship("Appartment", back_populates="BuildCharac_table")
    
class LeaseRentCharges(Base):
    __tablename__ = 'lease_rent_charges'
    
    rent_id = Column(Integer, primary_key=True)
    flat_id = Column(Integer, ForeignKey('appartment.id', ondelete='CASCADE'))
    type_of_lease = Column(String(256))
    lease_duration = Column(String(255))
    rent_charges = Column(String(255))
    additional_rent = Column(String(255))
    tenant_fess = Column(String(255))
    charge_provision = Column(String(255))
    check_in_fees = Column(String(255))
    security_deposit = Column(String(255))
    availability = Column(String(255))
    appart_table = relationship("Appartment", back_populates="Lease_rent_table")
    
class PropertyCharacteristics(Base):
    __tablename__ = 'property_characteristics'
    
    proper_charac_id = Column(Integer, primary_key=True)
    flat_id = Column(Integer, ForeignKey('appartment.id', ondelete='CASCADE'))
    Floor = Column(String(10))
    Total_area = Column(Float)
    Living_area = Column(Float)
    Number_of_rooms = Column(Integer)
    Number_of_bedrooms = Column(Integer)
    Number_of_bathrooms = Column(Integer)
    Hot_water_system = Column(String(45))
    Heating_system = Column(String(45))
    Double_glazing = Column(String(45))
    appart_table = relationship("Appartment", back_populates="PropertyCharac_table")