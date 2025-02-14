from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ContractTypes(Base):
    __tablename__ = 'ContractTypes'
    
    ContractTypeId = Column(Integer, primary_key=True)
    ContractType = Column(String)
    ContractSubType = Column(String)
    ContractOwner = Column(String)
    ContractOwnerEmail = Column(String)
    DaysBeforeReminder = Column(Integer)
    DocumentType = Column(String)
