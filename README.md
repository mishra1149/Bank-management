# Bank-management
# 🏦 Banking Management System

A simple **Banking Management System** built using **Python** and **JSON file handling**.
This project allows users to create a bank account, deposit money, and store account information permanently in a JSON file.

## 📌 Features

* Create a new bank account
* Generate a random account number
* Set a 4-digit PIN
* Check account age eligibility
* Deposit money
* Validate account number and PIN
* Maintain account balance
* Store data permanently in `data.json`
* Load existing account data when the program starts

## 🛠️ Technologies Used

* **Python**
* **JSON**
* **Random**
* **String**
* **Pathlib**
* **Object-Oriented Programming (OOP)**
* **File Handling**

## 📂 Project Structure

```text
Banking-Management-System/
│
├── bank.py
├── data.json
└── README.md
```

## ⚙️ How It Works

When the program starts, it checks whether `data.json` exists.

If the file exists, the existing bank account data is loaded into the program.

If a new account is created, the account information is stored in the JSON file.

Example account data:

```json
[
    {
        "name": "mishra",
        "age": 71,
        "email": "vm1149",
        "pin": 9899,
        "accountNo.": "%qo60c",
        "balance": 500
    }
]
```

## 🏦 Available Operations

The program provides the following options:

```text
1. Create an account
2. Deposit money
3. Withdraw money
4. Account details
5. Update details
6. Delete an account
```

> Currently, account creation and money deposit functionality have been implemented. Other menu options can be added in future versions.

## 💰 Deposit Money

To deposit money, the user needs to provide:

* Account number
* 4-digit PIN
* Deposit amount

The program verifies the account number and PIN before updating the balance.

The updated balance is then saved to `data.json`.

## 🔐 Account Validation

The program checks:

* Age must be 18 or above
* PIN must contain exactly 4 digits
* Account number and PIN must match during deposit
* Deposit amount must be greater than `0`
* Maximum deposit amount is `10,000`

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Open the project folder

```bash
cd Banking-Management-System
```

### 3. Run the Python program

```bash
python bank.py
```

## 📚 Concepts Practiced

This project was created to practice important Python concepts such as:

* Classes and Objects
* Class Methods
* Lists and Dictionaries
* List Comprehension
* Conditional Statements
* Functions
* Exception Handling
* File Handling
* JSON
* Random Data Generation
* Data Persistence

## 🚀 Future Improvements

The following features can be added in future versions:

* Withdraw money
* View account details
* Update account information
* Delete account
* Transaction history
* Balance checking
* Multiple user accounts
* Improved PIN validation
* Better error handling
* Login system
* Transaction receipts

## 👨‍💻 Author

**Vishnu Mishra**

This project was developed as a Python practice project to understand **OOP, file handling, JSON, and basic banking operations**.
