<img src='https://github.com/Soshtakovich/XEX_BANK_APP/blob/main/static/assets/imgz/logo.png'>

# XEX BANK

## Project Description

XEX BANK is an online banking system designed to provide users with a secure and user-friendly platform to manage their financial transactions. Users can view balances, transfer funds, and withdraw money from various accounts including Debit, Savings, Investments, and Credit Card accounts.

1. Deployed Site: [XEX BANK](https://banking.zakesmatsimbe.tech/)
2. Final Project Blog Article: [Blog Post](https://www.linkedin.com/pulse/xex-bank-project-zakes-matsimbe-omqpf/)
3. Author LinkedIn: [Zakes Matsimbe](www.linkedin.com/in/zakes-matsimbe-004722270)

## Features
- View Account Balances
- Transfer money between accounts
- Withdraw money from account (Generate a code to withdraw from ATM)
- View Transactons and their details

## Installation
1. Clone the repository
    ```bash
    git clone https://github.com/Soshtakovich/XEX_BANK_APP.git
    ```
2. Navigate to the project directory
    ```bash
    cd XEX_BANK_APP
    ```
3. Set up a virtual environment
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
4. Install the required dependencies
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Run the Flask app
    ```bash
    flask run
    ```
2. Open your browser and go to `http://127.0.0.1:5000`

## APIs
- **Fetch user info**: `/api/user`
- **Fetch accounts and their balances**: `/api/accounts`
- **Fetch transactions of a user**: `/api/transactions`
- **Fetch credit and investments details for a user**: `/api/credit_investments`

## Project Structure
- **app.py**: Main application file
- **templates/**: HTML templates
- **static/**: Static files (CSS, JavaScript, images)
- **connect.py   |   db_functions.py   |   fetch_acc.py   |   transact.py**: Python scripts for backend functionality

## Contributing
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some feature'`)
5. Push to the branch (`git push origin feature-branch`)
6. Open a pull request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
- **Name**: Zakes Matsimbe
- **Email**: soshtakovichtech@gmail.com
- **GitHub**: [Soshtakovich](https://github.com/Soshtakovich)

