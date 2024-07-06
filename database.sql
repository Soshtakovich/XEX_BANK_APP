
-- Drop existing database if it exists
DROP DATABASE IF EXISTS banking;

-- Create new database
CREATE DATABASE banking;

USE banking;
-- Drop existing tables if they exist
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Accounts;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Transfers;
DROP TABLE IF EXISTS Credits;
DROP TABLE IF EXISTS Investments;

-- Create Users table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    id_number VARCHAR(13) NOT NULL,
    username VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    name_s VARCHAR(50) NOT NULL,
    age VARCHAR(10) NOT NULL,
    date_of_birth VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(10),
    address VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Accounts table
CREATE TABLE Accounts (
    account_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    account_type VARCHAR(50),
    account_no VARCHAR(50) UNIQUE,
    balance DECIMAL(10, 2) DEFAULT 0.00,
    available_balance DECIMAL(10, 2) DEFAULT 0.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Create Transactions table
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    transaction_type VARCHAR(50),
    amount DECIMAL(10, 2),
    description TEXT,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

-- Create Transfers table
CREATE TABLE Transfers (
    transfer_id INT AUTO_INCREMENT PRIMARY KEY,
    from_account_id INT,
    to_account_id INT,
    amount DECIMAL(10, 2),
    transfer_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (from_account_id) REFERENCES Accounts(account_id),
    FOREIGN KEY (to_account_id) REFERENCES Accounts(account_id)
);

-- Create Credits table
CREATE TABLE Credits (
    credit_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    credit_available DECIMAL(10, 2),
    owing DECIMAL(10, 2),
    expected_repayment DECIMAL(10, 2),
    term VARCHAR(50),
    interest_rate DECIMAL(5, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

-- Create Investments table
CREATE TABLE Investments (
    investment_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    principal DECIMAL(10, 2),
    balance DECIMAL(10, 2),
    installment DECIMAL(10, 2),
    term VARCHAR(50),
    interest_rate DECIMAL(5, 2),
    expected_return DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

