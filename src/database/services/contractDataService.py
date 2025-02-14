from sqlalchemy.orm import Session
from database.models.ContractDataModel import ContractData

class ContractDataService:
    def __init__(self, session: Session):
        self.session = session
    
    def get_unprocessed_contracts(self, ContractId: int):
        unprocessed_contracts = self.session.query(ContractData).filter(ContractData.ContractId == ContractId).all()
        return unprocessed_contracts


