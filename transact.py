from flask import Flask, request, session, jsonify
from connect import get_db_connection
import random
import logging

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def transfer():
    data = request.get_json()

    if not data:
        logging.error('Invalid JSON input')
        return jsonify({'success': False, 'message': 'Invalid JSON input'})

    from_account = data.get('fromAccount')
    to_account = data.get('toAccount')
    amount = data.get('amount')

    if not from_account or not to_account or not amount:
        logging.error('Missing fields in input')
        return jsonify({'success': False, 'message': 'Please fill in all fields'})

    db = None
    cursor = None

    try:
        db = get_db_connection()
        cursor = db.cursor()
        logging.debug(f"DB Connection: {db}")
        logging.debug(f"Session User ID: {session.get('user_id')}")

        # Start transaction explicitly
        cursor.execute("START TRANSACTION")
        logging.debug("Transaction started")

        # Check balance in the fromAccount
        cursor.execute("SELECT balance FROM Accounts WHERE account_type = %s AND user_id = %s FOR UPDATE", (from_account, session['user_id']))
        row = cursor.fetchone()
        logging.debug(f"Balance Check: {row}")

        if not row or row['balance'] < amount:
            logging.error('Insufficient funds or invalid account')
            return jsonify({'success': False, 'message': 'Insufficient funds or invalid account'})

        # Deduct amount from fromAccount
        cursor.execute("UPDATE Accounts SET balance = balance - %s WHERE account_type = %s AND user_id = %s", (amount, from_account, session['user_id']))
        logging.debug("Amount deducted from from_account")

        # Add amount to toAccount
        cursor.execute("UPDATE Accounts SET balance = balance + %s WHERE account_type = %s AND user_id = %s", (amount, to_account, session['user_id']))
        logging.debug("Amount added to to_account")

        # Insert transaction record
        description = f"Transfer from {from_account} to {to_account}"
        cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount, description) VALUES ((SELECT account_id FROM Accounts WHERE account_type = %s AND user_id = %s), 'Cash Transfer', %s, %s)", (from_account, session['user_id'], amount, description))
        logging.debug("Transaction record inserted")

        # Commit transaction
        db.commit()
        logging.debug("Transaction committed")
        return jsonify({'success': True})

    except Exception as e:
        if db:
            db.rollback()
        logging.error(f"Exception: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def withdraw():
    data = request.get_json()

    if not data:
        logging.error('Invalid JSON input')
        return jsonify({'success': False, 'message': 'Invalid JSON input'})

    from_account = data.get('fromAccount')
    amount = data.get('amount')

    if not from_account or not amount:
        logging.error('Missing fields in input')
        return jsonify({'success': False, 'message': 'Please fill in all fields'})

    db = None
    cursor = None

    try:
        db = get_db_connection()
        cursor = db.cursor()
        logging.debug(f"DB Connection: {db}")
        logging.debug(f"Session User ID: {session.get('user_id')}")

        # Start transaction explicitly
        cursor.execute("START TRANSACTION")
        logging.debug("Transaction started")

        # Check balance in the fromAccount
        cursor.execute("SELECT balance FROM Accounts WHERE account_type = %s AND user_id = %s FOR UPDATE", (from_account, session['user_id']))
        row = cursor.fetchone()
        logging.debug(f"Balance Check: {row}")

        if not row or row['balance'] < amount:
            logging.error('Insufficient funds or invalid account')
            return jsonify({'success': False, 'message': 'Insufficient funds or invalid account'})

        # Deduct amount from fromAccount
        cursor.execute("UPDATE Accounts SET balance = balance - %s WHERE account_type = %s AND user_id = %s", (amount, from_account, session['user_id']))
        logging.debug("Amount deducted from from_account")

        # Insert withdrawal transaction record
        description = "Cash Withdrawal"
        cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount, description) VALUES ((SELECT account_id FROM Accounts WHERE account_type = %s AND user_id = %s), 'Withdrawal', %s, %s)", (from_account, session['user_id'], amount, description))
        logging.debug("Withdrawal transaction record inserted")

        # Simulate sending email with withdrawal code
        code = f'XEXWITHDR-{random.randint(100000, 999999)}'
        user_email = fetch_user_email(session['user_id'])
        if user_email:
            code = f'XEXWITHDR-{random.randint(100000, 999999)}'
            logging.debug(f"Generated withdrawal code: {code}")
            # Replace with actual email sending code
            #print(f"Sending email to {user_email}: Your withdrawal code is {code}")
            # Include withdrawal code in response
            #return jsonify({'success': True, 'withdrawalCode': code})

        # Commit transaction
        db.commit()
        logging.debug("Transaction committed")
        return jsonify({'success': True, 'withdrawalCode': code})

    except Exception as e:
        if db:
            db.rollback()
        logging.error(f"Exception: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def fetch_user_email(user_id):
    db = None
    cursor = None

    try:
        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT email FROM Users WHERE user_id = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            return row[0]
        return None

    except Exception as e:
        return None

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
