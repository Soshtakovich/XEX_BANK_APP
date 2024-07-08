from flask import Flask, request, session, jsonify
from connect import get_db_connection
import random

app = Flask(__name__)
app.secret_key = '##################'

def transfer():
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON input'})

    from_account = data.get('fromAccount')
    to_account = data.get('toAccount')
    amount = data.get('amount')

    if not from_account or not to_account or not amount:
        logging.error('Missing fields in input')
        return jsonify({'success': False, 'message': 'Please fill in all fields'})

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("START TRANSACTION")
        cursor.execute("SELECT balance FROM Accounts WHERE account_type = %s AND user_id = %s FOR UPDATE", (from_account, session['user_id']))
        row = cursor.fetchone()

        if not row or row['balance'] < amount:
            return jsonify({'success': False, 'message': 'Insufficient funds or invalid account'})

        cursor.execute("UPDATE Accounts SET balance = balance - %s WHERE account_type = %s AND user_id = %s", (amount, from_account, session['user_id']))
        cursor.execute("UPDATE Accounts SET balance = balance + %s WHERE account_type = %s AND user_id = %s", (amount, to_account, session['user_id']))
        description = f"Transfer from {from_account} to {to_account}"
        cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount, description) VALUES ((SELECT account_id FROM Accounts WHERE account_type = %s AND user_id = %s), 'Cash Transfer', %s, %s)", (from_account, session['user_id'], amount, description))

        db.commit()
        return jsonify({'success': True})

    except Exception as e:
        if db:
            db.rollback()
        return jsonify({'success': False, 'message': str(e)})

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def withdraw():
    data = request.get_json()

    if not data:
        return jsonify({'success': False, 'message': 'Invalid JSON input'})

    from_account = data.get('fromAccount')
    amount = data.get('amount')

    if not from_account or not amount:
        return jsonify({'success': False, 'message': 'Please fill in all fields'})

    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("START TRANSACTION")

        cursor.execute("SELECT balance FROM Accounts WHERE account_type = %s AND user_id = %s FOR UPDATE", (from_account, session['user_id']))
        row = cursor.fetchone()

        if not row or row['balance'] < amount:
            return jsonify({'success': False, 'message': 'Insufficient funds or invalid account'})

        cursor.execute("UPDATE Accounts SET balance = balance - %s WHERE account_type = %s AND user_id = %s", (amount, from_account, session['user_id']))

        description = "Cash Withdrawal"
        cursor.execute("INSERT INTO Transactions (account_id, transaction_type, amount, description) VALUES ((SELECT account_id FROM Accounts WHERE account_type = %s AND user_id = %s), 'Withdrawal', %s, %s)", (from_account, session['user_id'], amount, description))

        code = f'XEXWITHDR-{random.randint(100000, 999999)}'
        user_email = fetch_user_email(session['user_id'])
        if user_email:
            code = f'XEXWITHDR-{random.randint(100000, 999999)}'

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
