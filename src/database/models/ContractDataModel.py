import sqlalchemy as sa 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ContractData(Base):
    __tablename__ = "ContractData"

    ContractId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    VendorName = sa.Column(sa.String(255), nullable=False)
    VendorNumber = sa.Column(sa.String(100), nullable=True)
    DocumentType = sa.Column(sa.String(100), nullable=True)
    ContractNumber = sa.Column(sa.String(100), nullable=True)
    DocDate = sa.Column(sa.Date, nullable=True)
    Title = sa.Column(sa.String(255), nullable=True)
    ExpirationDate = sa.Column(sa.Date, nullable=True)
    ContractSummary = sa.Column(sa.Text, nullable=True)

