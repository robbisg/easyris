import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Patient(Base):
    
    __tablename__ = 'patient'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    birthplace = Column(String(250))
    birthdate = Column(DateTime)
    codicefiscale = Column(String(15))
    parentsurname = Column(String(50), nullable=True)
    parentname = Column(String(50), nullable=True)
    address = Column(String(50))
    city = Column(String(50))
    province = Column(String(2))
    cap = Column(String(5))
    phone = Column(String(20))
    email = Column(String(50))
    medico_id = Column(Integer, ForeignKey('medico.id'))
    note = Column(String(250))

class Medico(Base):
    
    __tablename__ = 'medico'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    address = Column(String(50))
    city = Column(String(50))
    province = Column(String(2))
    cap = Column(String(5))
    phone = Column(String(20))
    email = Column(String(50))
    
    
    
    
    
    
    
    
    