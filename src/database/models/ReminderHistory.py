import sqlalchemy as sa 
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ReminderHistory(Base):
    __tablename__ = 'ReminderHistory'
    
    ReminderId = sa.Column(sa.Integer, primary_key=True, autoincrement=True)  
    ContractID = sa.Column(sa.Integer, nullable=False)                       
    IsReminderSent = sa.Column(sa.Boolean, nullable=False)                   
    ReminderDate = sa.Column(sa.Date, nullable=False)                        