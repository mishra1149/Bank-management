import streamlit as st
import json
import random
import string
from pathlib import Path


class BANK:

    database = "data.json"
    data = []

    # ---------------- LOAD DATA ----------------
    @classmethod
    def load_data(cls):
        try:
            if Path(cls.database).exists():
                with open(cls.database, "r") as fs:
                    cls.data = json.load(fs)
            else:
                cls.data = []

        except Exception as err:
            st.error(f"Error loading database: {err}")
            cls.data = []

    # ---------------- UPDATE JSON ----------------
    @classmethod
    def update(cls):
        try:
            with open(cls.database, "w") as fs:
                json.dump(cls.data, fs, indent=4)

        except Exception as err:
            st.error(f"Error updating database: {err}")

    # ---------------- ACCOUNT NUMBER ----------------
    @classmethod
    def account_generate(cls):

        while True:

            alpha = random.choices(string.ascii_uppercase, k=3)
            num = random.choices(string.digits, k=2)
            special = random.choices("!@#$%^&*", k=1)

            account = alpha + num + special

            random.shuffle(account)

            account_number = "".join(account)

            # Check duplicate account number
            if not any(
                user["accountNo."] == account_number
                for user in cls.data
            ):
                return account_number

    # ---------------- FIND USER ----------------
    @classmethod
    def find_user(cls, account_number, pin):

        return next(
            (
                user
                for user in cls.data
                if user["accountNo."] == account_number
                and user["pin"] == pin
            ),
            None
        )

    # ---------------- CREATE ACCOUNT ----------------
    @classmethod
    def create_account(cls, name, age, email, pin):

        if age < 18:
            return False, "You must be 18 or older."

        if len(str(pin)) != 4:
            return False, "PIN must contain exactly 4 digits."

        if not str(pin).isdigit():
            return False, "PIN must contain only numbers."

        account_number = cls.account_generate()

        info = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountNo.": account_number,
            "balance": 0
        }

        cls.data.append(info)
        cls.update()

        return True, info

    # ---------------- DEPOSIT ----------------
    @classmethod
    def deposit(cls, account_number, pin, amount):

        user = cls.find_user(account_number, pin)

        if user is None:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Deposit amount must be greater than 0."

        if amount > 10000:
            return False, "You can deposit maximum ₹10,000 at a time."

        user["balance"] += amount

        cls.update()

        return True, user["balance"]

    # ---------------- WITHDRAW ----------------
    @classmethod
    def withdraw(cls, account_number, pin, amount):

        user = cls.find_user(account_number, pin)

        if user is None:
            return False, "Invalid account number or PIN."

        if amount <= 0:
            return False, "Withdrawal amount must be greater than 0."

        if amount > user["balance"]:
            return False, "Insufficient balance."

        user["balance"] -= amount

        cls.update()

        return True, user["balance"]

    # ---------------- SHOW DETAILS ----------------
    @classmethod
    def get_details(cls, account_number, pin):

        user = cls.find_user(account_number, pin)

        if user is None:
            return None

        return user

    # ---------------- UPDATE DETAILS ----------------
    @classmethod
    def update_details(
        cls,
        account_number,
        pin,
        name,
        email,
        new_pin
    ):

        user = cls.find_user(account_number, pin)

        if user is None:
            return False, "Invalid account number or PIN."

        if name:
            user["name"] = name

        if email:
            user["email"] = email

        if new_pin:

            if len(new_pin) != 4 or not new_pin.isdigit():
                return False, "New PIN must contain exactly 4 digits."

            user["pin"] = int(new_pin)

        cls.update()

        return True, "Details updated successfully."

    # ---------------- DELETE ACCOUNT ----------------
    @classmethod
    def delete_account(cls, account_number, pin):

        user = cls.find_user(account_number, pin)

        if user is None:
            return False, "Invalid account number or PIN."

        cls.data.remove(user)

        cls.update()

        return True, "Account deleted successfully."


# Load database
BANK.load_data()


# ==================================================
# STREAMLIT UI
# ==================================================

st.set_page_config(
    page_title="Bank Management System",
    page_icon="🏦",
    layout="centered"
)

st.title("🏦 Bank Management System")

st.sidebar.title("Bank Menu")

option = st.sidebar.selectbox(
    "Choose Operation",
    [
        "Create Account",
        "Deposit Money",
        "Withdraw Money",
        "Account Details",
        "Update Details",
        "Delete Account"
    ]
)


# ==================================================
# CREATE ACCOUNT
# ==================================================

if option == "Create Account":

    st.header("📝 Create New Account")

    with st.form("create_account_form"):

        name = st.text_input("Enter your name")

        age = st.number_input(
            "Enter your age",
            min_value=1,
            max_value=120,
            step=1
        )

        email = st.text_input("Enter your email")

        pin = st.text_input(
            "Create 4 digit PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button("Create Account")

        if submit:

            if not name or not email or not pin:
                st.error("Please fill all fields.")

            elif not pin.isdigit():
                st.error("PIN must contain numbers only.")

            else:

                success, result = BANK.create_account(
                    name,
                    age,
                    email,
                    int(pin)
                )

                if success:

                    st.success("Account created successfully! 🎉")

                    st.write("### Account Information")

                    st.write(f"**Name:** {result['name']}")
                    st.write(f"**Age:** {result['age']}")
                    st.write(f"**Email:** {result['email']}")
                    st.write(f"**Account Number:** `{result['accountNo.']}`")
                    st.write(f"**Balance:** ₹{result['balance']}")

                    st.warning(
                        f"Please save your account number: "
                        f"{result['accountNo.']}"
                    )

                else:
                    st.error(result)


# ==================================================
# DEPOSIT
# ==================================================

elif option == "Deposit Money":

    st.header("💰 Deposit Money")

    with st.form("deposit_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        amount = st.number_input(
            "Deposit Amount",
            min_value=0,
            step=100
        )

        submit = st.form_submit_button("Deposit Money")

        if submit:

            if not account_number or not pin:
                st.error("Please enter account number and PIN.")

            elif not pin.isdigit():
                st.error("Invalid PIN.")

            else:

                success, result = BANK.deposit(
                    account_number,
                    int(pin),
                    amount
                )

                if success:
                    st.success("Amount deposited successfully! ✅")
                    st.metric("Current Balance", f"₹{result}")

                else:
                    st.error(result)


# ==================================================
# WITHDRAW
# ==================================================

elif option == "Withdraw Money":

    st.header("💸 Withdraw Money")

    with st.form("withdraw_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        amount = st.number_input(
            "Withdrawal Amount",
            min_value=0,
            step=100
        )

        submit = st.form_submit_button("Withdraw Money")

        if submit:

            if not account_number or not pin:
                st.error("Please enter account number and PIN.")

            elif not pin.isdigit():
                st.error("Invalid PIN.")

            else:

                success, result = BANK.withdraw(
                    account_number,
                    int(pin),
                    amount
                )

                if success:
                    st.success("Amount withdrawn successfully! ✅")
                    st.metric("Remaining Balance", f"₹{result}")

                else:
                    st.error(result)


# ==================================================
# ACCOUNT DETAILS
# ==================================================

elif option == "Account Details":

    st.header("👤 Account Details")

    with st.form("details_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        submit = st.form_submit_button(
            "Show Details"
        )

        if submit:

            if not pin.isdigit():
                st.error("Invalid PIN.")

            else:

                user = BANK.get_details(
                    account_number,
                    int(pin)
                )

                if user is None:

                    st.error(
                        "Invalid account number or PIN."
                    )

                else:

                    st.success("Account found! ✅")

                    st.write(
                        f"### Welcome, {user['name']} 👋"
                    )

                    col1, col2 = st.columns(2)

                    with col1:

                        st.write(
                            f"**Name:** {user['name']}"
                        )

                        st.write(
                            f"**Age:** {user['age']}"
                        )

                        st.write(
                            f"**Email:** {user['email']}"
                        )

                    with col2:

                        st.write(
                            f"**Account No.:** "
                            f"`{user['accountNo.']}`"
                        )

                        st.write(
                            f"**Balance:** ₹{user['balance']}"
                        )


# ==================================================
# UPDATE DETAILS
# ==================================================

elif option == "Update Details":

    st.header("✏️ Update Account Details")

    st.info(
        "You can update name, email and PIN. "
        "Age, account number and balance cannot be changed."
    )

    with st.form("update_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "Current PIN",
            type="password",
            max_chars=4
        )

        new_name = st.text_input(
            "New Name",
            placeholder="Leave empty if no change"
        )

        new_email = st.text_input(
            "New Email",
            placeholder="Leave empty if no change"
        )

        new_pin = st.text_input(
            "New PIN",
            type="password",
            max_chars=4,
            placeholder="Leave empty if no change"
        )

        submit = st.form_submit_button(
            "Update Details"
        )

        if submit:

            if not pin.isdigit():
                st.error("Invalid current PIN.")

            else:

                success, message = BANK.update_details(
                    account_number,
                    int(pin),
                    new_name,
                    new_email,
                    new_pin
                )

                if success:
                    st.success(message)

                else:
                    st.error(message)


# ==================================================
# DELETE ACCOUNT
# ==================================================

elif option == "Delete Account":

    st.header("🗑️ Delete Account")

    st.warning(
        "⚠️ This action is permanent. "
        "Your account cannot be recovered after deletion."
    )

    with st.form("delete_form"):

        account_number = st.text_input(
            "Account Number"
        )

        pin = st.text_input(
            "PIN",
            type="password",
            max_chars=4
        )

        confirm = st.checkbox(
            "I understand that my account will be permanently deleted."
        )

        submit = st.form_submit_button(
            "Delete Account"
        )

        if submit:

            if not confirm:

                st.error(
                    "Please confirm account deletion."
                )

            elif not pin.isdigit():

                st.error("Invalid PIN.")

            else:

                success, message = BANK.delete_account(
                    account_number,
                    int(pin)
                )

                if success:
                    st.success(message)

                else:
                    st.error(message)