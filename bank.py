import sqlite3

conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    balance REAL NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id INTEGER,
    type TEXT,
    amount REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


def create_account():
    name = input("Enter account holder name: ")
    deposit = float(input("Enter initial deposit: $"))
    if deposit < 0:
        print("Initial deposit can't be negative.")
        return
    cursor.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, deposit))
    conn.commit()
    cursor.execute("SELECT last_insert_rowid()")
    account_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)", (account_id, "deposit", deposit))
    conn.commit()
    print(f"Account created! Account ID: {account_id}")


def deposit():
    account_id = int(input("Enter account ID: "))
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    account = cursor.fetchone()
    if not account:
        print("Account not found.")
        return
    amount = float(input("Enter deposit amount: $"))
    if amount <= 0:
        print("Amount must be positive.")
        return
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)", (account_id, "deposit", amount))
    conn.commit()
    print(f"Deposited ${amount:.2f}. New balance: ${account[2] + amount:.2f}")


def withdraw():
    account_id = int(input("Enter account ID: "))
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    account = cursor.fetchone()
    if not account:
        print("Account not found.")
        return
    amount = float(input("Enter withdrawal amount: $"))
    if amount <= 0:
        print("Amount must be positive.")
        return
    if amount > account[2]:
        print("Insufficient funds.")
        return
    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, account_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)", (account_id, "withdrawal", amount))
    conn.commit()
    print(f"Withdrew ${amount:.2f}. New balance: ${account[2] - amount:.2f}")


def check_balance():
    account_id = int(input("Enter account ID: "))
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    account = cursor.fetchone()
    if not account:
        print("Account not found.")
        return
    print(f"Account: {account[1]} | Balance: ${account[2]:.2f}")


def list_accounts():
    cursor.execute("SELECT * FROM accounts")
    accounts = cursor.fetchall()
    if not accounts:
        print("No accounts found.")
        return
    print(f"\n{'ID':<6} {'Name':<20} {'Balance':>10}")
    print("-" * 38)
    for a in accounts:
        print(f"{a[0]:<6} {a[1]:<20} ${a[2]:>9.2f}")
    print()


def transaction_history():
    account_id = int(input("Enter account ID: "))
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (account_id,))
    account = cursor.fetchone()
    if not account:
        print("Account not found.")
        return
    cursor.execute("SELECT type, amount, timestamp FROM transactions WHERE account_id = ? ORDER BY timestamp DESC", (account_id,))
    txns = cursor.fetchall()
    if not txns:
        print("No transactions found.")
        return
    print(f"\nTransaction history for {account[1]}:")
    print(f"{'Type':<12} {'Amount':>10}  {'Time'}")
    print("-" * 45)
    for t in txns:
        print(f"{t[0]:<12} ${t[1]:>9.2f}  {t[2]}")
    print()


def wire_transfer():
    from_id = int(input("Enter sender account ID: "))
    to_id = int(input("Enter receiver account ID: "))
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (from_id,))
    sender = cursor.fetchone()
    cursor.execute("SELECT * FROM accounts WHERE id = ?", (to_id,))
    receiver = cursor.fetchone()
    if not sender or not receiver:
        print("One or both accounts not found.")
        return
    amount = float(input("Enter transfer amount: $"))
    if amount <= 0:
        print("Amount must be positive.")
        return
    if amount > sender[2]:
        print("Insufficient funds.")
        return
    cursor.execute("UPDATE accounts SET balance = balance - ? WHERE id = ?", (amount, from_id))
    cursor.execute("UPDATE accounts SET balance = balance + ? WHERE id = ?", (amount, to_id))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)", (from_id, "transfer out", amount))
    cursor.execute("INSERT INTO transactions (account_id, type, amount) VALUES (?, ?, ?)", (to_id, "transfer in", amount))
    conn.commit()
    print(f"Transferred ${amount:.2f} from account {from_id} to account {to_id}.")


def menu():
    while True:
        print("\n=============================")
        print("     ELITE 102 BANK APP      ")
        print("=============================")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. List All Accounts")
        print("6. Transaction History")
        print("7. Wire Transfer")
        print("8. Exit")
        print("=============================")
        choice = input("Choose an option: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            list_accounts()
        elif choice == "6":
            transaction_history()
        elif choice == "7":
            wire_transfer()
        elif choice == "8":
            print("Goodbye!")
            conn.close()
            break
        else:
            print("Invalid option, try again.")

menu()
