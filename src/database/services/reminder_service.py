from sqlalchemy import text
from database.db_connection import get_db_session
from database.models.ContractDataModel import ContractData


# If you need to use raw SQL queries:
def query_database_raw():
    session = get_db_session()
    try:
        result = session.execute(
            text("SELECT TOP 10 * FROM ContractData")
        )
        return result.fetchall()
    except Exception as e:
        print(f"Error fetching data: {e}")
        raise
    finally:
        session.close()

def query_contract_data():
    session = get_db_session()
    try:
        # Query all rows from the ContractData table
        contract_data_objects = session.query(ContractData).all()
        
        # Iterate over the results and print each object
        for contract in contract_data_objects:
            print(f"Contract ID: {contract.contractId}, Vendor Name: {contract.VendorName}")
            # You can access other fields similarly
            # Example: print(contract.VendorNumber, contract.DocumentType, etc.)
        
        return contract_data_objects
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()

