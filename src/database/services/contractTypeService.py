from database.models.ContractTypesModel import ContractTypes
from sqlalchemy.orm import Session

class ContractTypeService:
    def __init__(self, session: Session):
        self.session = session

    def get_contract_type_days_before_reminder(self, contract_type_id: int):
        contract_type = self.session.query(ContractTypes).filter(ContractTypes.ContractTypeId == contract_type_id).first()
        return contract_type.DaysBeforeReminder
    
    def get_contract_type(self, contract_type_id: int):
        contract_type = self.session.query(ContractTypes).filter(ContractTypes.ContractTypeId == contract_type_id).first()
        return contract_type


