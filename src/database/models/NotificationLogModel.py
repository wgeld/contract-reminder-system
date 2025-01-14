import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NotificationLog(Base):
    __tablename__ = "NotificationLog"
    
    NotificationId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ContractId = sa.Column(sa.Integer, nullable=False)
    CreatedAt = sa.Column(sa.DateTime, nullable=True)
    Processed = sa.Column(sa.Boolean, nullable=True)