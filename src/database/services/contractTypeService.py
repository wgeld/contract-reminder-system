from database.models.ContractTypesModel import ContractTypes
from sqlalchemy.orm import Session

class ContractTypeService:
    def __init__(self, session: Session):
        self.session = session

    def get_contract_type(self, contract_type_id: int):
        return self.session.query(ContractTypes).filter(ContractTypes.ContractTypeId == contract_type_id).first()


