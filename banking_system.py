import random
from datetime import datetime

# Stores all bank accounts while the program is running.
accounts = {}


def generate_account_number():
    """Generate a unique 8-digit account number."""
    while True:
        account_number = str(random.randint(10000000, 99999999))
        if account_number not in accounts:
            return account_number


def add_transaction(account, message):
    """Add a date/time-stamped transaction to an account."""
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    account["transactions"].append(f"{timestamp} - {message}")


def create_account():
    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    phone = input("Enter phone number: ").strip()
    if not phone.isdigit() or len(phone) != 10:
        print("Please enter a valid 10-digit phone number.")
        return

    pin = input("Create a 4-digit PIN: ").strip()
    if not pin.isdigit() or len(pin) != 4:
        print("PIN must contain exactly 4 digits.")
        return

    confirm_pin = input("Confirm PIN: ").strip()
    if pin != confirm_pin:
        print("PINs do not match.")
        return

    account_number = generate_account_number()

    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }

    add_transaction(accounts[account_number], "Account created")

    print("\nAccount created successfully!")
    print(f"Account Number: {account_number}")
    print("Please remember your account number and PIN.")


def login():
    print("\n=============== LOGIN ===============")

    account_number = input("Enter account number: ").strip()
    pin = input("Enter PIN: ").strip()

    account = accounts.get(account_number)

    if account is None:
        print("Account not found.")
        return

    if account["pin"] != pin:
        print("Incorrect PIN.")
        return

    print(f"\nWelcome, {account['name']}!")
    account_menu(account_number)


def check_balance(account):
    print("\n========== ACCOUNT BALANCE ==========")
    print(f"Available Balance: ₹{account['balance']:.2f}")


def deposit(account):
    print("\n============== DEPOSIT ==============")

    amount_text = input("Enter amount to deposit: ").strip()

    try:
        amount = float(amount_text)
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    account["balance"] += amount
    add_transaction(account, f"Deposited ₹{amount:.2f}")

    print(f"₹{amount:.2f} deposited successfully.")
    print(f"New Balance: ₹{account['balance']:.2f}")


def withdraw(account):
    print("\n============= WITHDRAW =============")

    amount_text = input("Enter amount to withdraw: ").strip()

    try:
        amount = float(amount_text)
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > account["balance"]:
        print("Insufficient balance.")
        return

    account["balance"] -= amount
    add_transaction(account, f"Withdrawn ₹{amount:.2f}")

    print(f"₹{amount:.2f} withdrawn successfully.")
    print(f"New Balance: ₹{account['balance']:.2f}")


def transfer(sender_account_number, sender):
    print("\n============= TRANSFER =============")

    receiver_number = input("Enter receiver account number: ").strip()

    if receiver_number == sender_account_number:
        print("You cannot transfer money to the same account.")
        return

    receiver = accounts.get(receiver_number)

    if receiver is None:
        print("Receiver account not found.")
        return

    amount_text = input("Enter amount to transfer: ").strip()

    try:
        amount = float(amount_text)
    except ValueError:
        print("Please enter a valid amount.")
        return

    if amount <= 0:
        print("Amount must be greater than zero.")
        return

    if amount > sender["balance"]:
        print("Insufficient balance.")
        return

    sender["balance"] -= amount
    receiver["balance"] += amount

    add_transaction(
        sender,
        f"Transferred ₹{amount:.2f} to Account {receiver_number}"
    )
    add_transaction(
        receiver,
        f"Received ₹{amount:.2f} from Account {sender_account_number}"
    )

    print(f"₹{amount:.2f} transferred successfully.")
    print(f"New Balance: ₹{sender['balance']:.2f}")


def transaction_history(account):
    print("\n========= TRANSACTION HISTORY =========")

    if not account["transactions"]:
        print("No transactions found.")
        return

    for number, transaction in enumerate(account["transactions"], start=1):
        print(f"{number}. {transaction}")


def change_pin(account):
    print("\n============= CHANGE PIN =============")

    old_pin = input("Enter old PIN: ").strip()

    if old_pin != account["pin"]:
        print("Incorrect old PIN.")
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()

    if not new_pin.isdigit() or len(new_pin) != 4:
        print("PIN must contain exactly 4 digits.")
        return

    confirm_pin = input("Confirm new PIN: ").strip()

    if new_pin != confirm_pin:
        print("New PINs do not match.")
        return

    if new_pin == old_pin:
        print("New PIN must be different from the old PIN.")
        return

    account["pin"] = new_pin
    add_transaction(account, "PIN changed")

    print("PIN changed successfully.")


def account_menu(account_number):
    account = accounts[account_number]

    while True:
        print("\n======================================")
        print("           ACCOUNT MENU")
        print("======================================")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            check_balance(account)
        elif choice == "2":
            deposit(account)
        elif choice == "3":
            withdraw(account)
        elif choice == "4":
            transfer(account_number, account)
        elif choice == "5":
            transaction_history(account)
        elif choice == "6":
            change_pin(account)
        elif choice == "7":
            print("\nLogged out successfully.")
            return
        else:
            print("Invalid choice. Please select 1-7.")


def main():
    while True:
        print("\n======================================")
        print("        PYTHON BANKING SYSTEM")
        print("======================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            create_account()
        elif choice == "2":
            login()
        elif choice == "3":
            print("\nThank you for using the Banking System.")
            break
        else:
            print("Invalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()
