import bcrypt
import random
import mysql.connector
from connect import get_db_connection
from flask import session



import logging

def validate_user(username, password):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT user_id, username, password, name_s, surname FROM Users WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    connection.close()
    
    if row:
        #print("Debug: Retrieved row from database:", row)  # Debug print
        if bcrypt.checkpw(password.encode('utf-8'), row['password'].encode('utf-8')):
            user = {
                'user_id': row['user_id'],
                'username': row['username'],
                'name_s': row['name_s'],
                'surname': row['surname']
            }
            # Storing user details in session
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            session['name_s'] = user['name_s']
            session['surname'] = user['surname']
            return user
        else:
            #print("Debug: Password check failed.")  # Debug print
    else:
        #print(f"Debug: No user found with username '{username}'.")  # Debug print
    
    return None



def generate_random_amount(min_amount, max_amount):
    return round(random.uniform(min_amount, max_amount), 2)

def generate_account_number(prefix):
    return f"{prefix}{''.join(random.choices('0123456789', k=10))}"

def generate_random_interest_rate(min_rate, max_rate):
    return round(random.uniform(min_rate, max_rate), 2)

def create_user(id_number, username, surname, name_s, age, date_of_birth, password, email, phone, address):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db = get_db_connection()
    cursor = db.cursor()

    try:
        # Begin transaction
        db.autocommit = False

        # Insert user into Users table
        insert_user_query = """
        INSERT INTO Users (id_number, username, surname, name_s, age, date_of_birth, password, email, phone, address)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_user_query, (id_number, username, surname, name_s, age, date_of_birth, hashed_password, email, phone, address))
        user_id = cursor.lastrowid

        # Insert accounts and set initial balances
        account_types = ['Debit', 'Savings', 'Credit', 'Investment']
        account_balances = {
            'Debit': generate_random_amount(100, 809),
            'Savings': generate_random_amount(0, 523),
            'Credit': generate_random_amount(0, 1200),
            'Investment': generate_random_amount(100, 3000)
        }

        for account_type in account_types:
            account_no = generate_account_number(account_type[:3])
            balance = account_balances[account_type]
            available_balance = balance if account_type != 'Credit' else generate_random_amount(600, 10000)

            insert_account_query = """
            INSERT INTO Accounts (user_id, account_type, account_no, balance, available_balance)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_account_query, (user_id, account_type, account_no, balance, available_balance))

            # Special handling for Credit and Investment accounts
            if account_type == 'Credit':
                account_id = cursor.lastrowid
                credit_available = generate_random_amount(600, 10000)
                owing = generate_random_amount(0, 5000)
                expected_repayment = generate_random_amount(500, 1500)
                term = random.randint(3, 24)
                interest_rate = generate_random_interest_rate(3, 11)

                insert_credit_query = """
                INSERT INTO Credits (account_id, credit_available, owing, expected_repayment, term, interest_rate)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_credit_query, (account_id, credit_available, owing, expected_repayment, term, interest_rate))

            elif account_type == 'Investment':
                account_id = cursor.lastrowid
                principal = generate_random_amount(1000, 50000)
                balance = principal
                term = random.randint(6, 72)
                interest_rate = generate_random_interest_rate(3.2, 5)
                installment = principal / term

                insert_investment_query = """
                INSERT INTO Investments (account_id, principal, balance, installment, term, interest_rate)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(insert_investment_query, (account_id, principal, balance, installment, term, interest_rate))

        # Commit transaction
        db.commit()
        return True
    except mysql.connector.Error as err:
        # Rollback transaction on error
        db.rollback()
        print(f"Error: {err}")
        return False
    finally:
        # Restore autocommit mode and clean up resources
        db.autocommit = True
        cursor.close()
        db.close()

def get_transactions(user_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
            SELECT t.transaction_id, a.account_type, t.transaction_type, t.amount, t.description, t.transaction_date 
            FROM Transactions t
            JOIN Accounts a ON t.account_id = a.account_id
            WHERE a.user_id = %s
            ORDER BY t.transaction_date DESC
        """

        cursor.execute(query, (user_id,))
        transactions = cursor.fetchall()

        #print(transactions)
        return transactions

    except mysql.connector.Error as e:
        return {'error': str(e)}
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
