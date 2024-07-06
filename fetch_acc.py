from connect import get_db_connection

def get_accounts(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
    SELECT account_id, account_type, available_balance, balance
    FROM Accounts
    WHERE user_id = %s
    """
    
    cursor.execute(query, (user_id,))
    accounts = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return accounts
