import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ContractTypes(Base):
    __tablename__ = "ContractTypes"
    
    ContractTypeId = sa.Column(sa.Integer, primary_key=True)
    ContractType = sa.Column(sa.String)
    ContractSubType = sa.Column(sa.String)
    ContractOwner = sa.Column(sa.String)
    ContractOwnerEmail = sa.Column(sa.String)
    DaysBeforeReminder = sa.Column(sa.Integer)
    DocumentType = sa.Column(sa.String)
