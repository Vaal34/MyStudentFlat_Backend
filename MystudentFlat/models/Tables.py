from sqlalchemy import Column, Integer, String, Text, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Appartment(Base):
    __tablename__ = 'appartment'
    
    flat_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    price = Column(Integer)
    ref = Column(Integer)
    description = Column(Text)
    square_meter = Column(Integer)
    address = Column(String(255))
    postal_code = Column(Integer)
    url = Column(String(255))

    lease_rent_charges = relationship("LeaseRentCharges", backref='appartment', cascade='all, delete')
    building_characteristics = relationship("BuildingCharacteristics", backref='appartment', cascade='all, delete')
    additional_surfaces = relationship("AdditionalSurfaces", backref='appartment', cascade='all, delete')
    amenities = relationship("Amenities", backref='appartment', cascade='all, delete')
    property_characteristics = relationship("PropertyCharacteristics", backref='appartment', cascade='all, delete')
    pictures = relationship("Pictures", backref='appartment', cascade='all, delete')

class AdditionalSurfaces(Base):
    __tablename__ = 'additional_surfaces'

    surface_id = Column(Integer, primary_key=True, autoincrement=True)
    flat_id = Column(Integer, ForeignKey('appartment.flat_id'))
    Cellar = Column(Integer)
    Private_parking = Column(Integer)

    appartment = relationship('Appartment', backref='additional_surfaces')

class Amenities(Base):
    __tablename__ = 'amenities'
    
    amenities_id = Column(Integer, primary_key=True, autoincrement=True)
    flat_id = Column(Integer, ForeignKey('appartment.flat_id'))
    Bathtub = Column(String(5))
    Kitchen_sink = Column(String(10))
    Washbasin = Column(String(5))
    Washing_machine_connection = Column(String(5))
    Ventilation_system = Column(String(5))
    TV_antenna = Column(String(5))

    appartment = relationship('Appartment', backref='amenities')

class BuildingCharacteristics(Base):
    __tablename__ = 'building_characteristics'
    
    building_charac_id = Column(Integer, primary_key=True, autoincrement=True)
    flat_id = Column(Integer, ForeignKey('appartment.flat_id'))
    Year_of_construction = Column(Integer)
    Number_of_Floor = Column(Integer)
    Digicode = Column(String(5))
    Videophone = Column(String(5))
    Elevator = Column(String(5))
    Green_peaces = Column(String(5))
    
    appartment = relationship('Appartment', backref='building_characteristics')

class LeaseRentCharges(Base):
    __tablename__ = 'lease_rent_charges'
    
    rent_id = Column(Integer, primary_key=True, autoincrement=True)
    flat_id = Column(Integer, ForeignKey('appartment.flat_id'))
    type_of_lease = Column(String(256))
    lease_duration = Column(String(255))
    rent_charges = Column(String(255))
    additional_rent = Column(String(255))
    tenant_fess = Column(String(255))
    charge_provision = Column(String(255))
    check_in_fees = Column(String(255))
    security_deposit = Column(String(255))
    availability = Column(String(255))
    
    appartment = relationship('Appartment', backref='lease_rent_charges')

class Pictures(Base):
    __tablename__ = 'pictures'
    
    picture_id = Column(Integer, primary_key=True, autoincrement=True)
    flat_id = Column(Integer, ForeignKey('appartment.flat_id'))
    picture_id = Column(Integer, primary_key=True)
    url_picture = Column(String(255))

    appartment = relationship('Appartment', backref='pictures')

class PropertyCharacteristics(Base):
    __tablename__ = 'property_characteristics'
    
    proper_charac_id = Column(Integer, primary_key=True, autoincrement=True)
    flat_id = Column(Integer, ForeignKey('appartment.flat_id'))
    Floor = Column(Integer)
    Total_area = Column(Integer)
    Living_area = Column(Integer)
    Number_of_rooms = Column(Integer)
    Number_of_bedrooms = Column(Integer)
    Number_of_bathrooms = Column(Integer)
    Hot_water_system = Column(String(45))
    Heating_system = Column(String(45))
    Double_glazing = Column(String(45))
    
    appartment = relationship('Appartment', backref='property_characteristics')