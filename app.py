from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from connect import get_db_connection
from transact import transfer, withdraw
from db_functions import validate_user, create_user, get_transactions
import random, fetch_acc, string
from flask_cors import CORS


app = Flask(__name__)
app.secret_key = '#################'
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = validate_user(username, password)
        if user:
            session['user_id'] = user['user_id']
            session['username'] = user['username']
            return jsonify({"success": True, "user_id": user['user_id']})
        else:
            return jsonify({"error": "Invalid username or password"})
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id_number = request.form['id_number']
        username = request.form['username']
        surname = request.form['surname']
        name_s = request.form['name_s']
        age = request.form['age']
        date_of_birth = request.form['date_of_birth']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        user_id = create_user(id_number, username, surname, name_s, age, date_of_birth, password, email, phone, address)
        if user_id:
            return jsonify({"success": True})
        else:
            return jsonify({"error": "Signup failed"})
    return render_template('signup.html')

@app.route('/bank')
def bank():
    
    return render_template('bank.html')

def generate_random_amount(min_val, max_val):
    return round(random.uniform(min_val, max_val), 2)



@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    user_info = {
        'name_s': session.get('name_s'),
        'surname': session.get('surname')
    }
    return jsonify(user_info)

@app.route('/get_accounts', methods=['GET'])
def get_accounts():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID not provided.'}), 400

    accounts = fetch_acc.get_accounts(user_id)
    if accounts:
        return jsonify(accounts)
    else:
        return jsonify({'error': 'No accounts found for the user.'}), 404


@app.route('/get_transactions', methods=['GET'])
def fetch_transactions():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'User session not found'}), 401

    user_id = session['user_id']
    transactions = get_transactions(user_id)

    if 'error' in transactions:
        return jsonify({'success': False, 'message': transactions['error']}), 500

    return jsonify({'success': True, 'transactions': transactions})

@app.route('/transfer', methods=['POST'])
def transfer_route():
    return transfer()

@app.route('/withdraw', methods=['POST'])
def withdraw_route():
    return withdraw()


@app.route('/logout')
def logout():
    # Clear session variables
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_surname', None)

    # Redirect to the home page or login page after logout
    return redirect(url_for('index_2'))

@app.route('/index_2')
def index_2():
    return render_template('index_2.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
