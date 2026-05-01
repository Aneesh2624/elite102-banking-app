# Elite 102 Banking App

A command-line banking system built with Python and SQLite.

## Features

- Create bank accounts with an initial deposit
- Deposit and withdraw money
- Check account balance
- List all accounts
- View transaction history with timestamps
- Wire transfer between accounts

## Setup

**Requirements:** Python 3 (SQLite is built in, nothing to install)

**Run the app:**
```bash
python3 bank.py
```

## Files

| File | Description |
|------|-------------|
| `bank.py` | Main app, run this to use the banking system |
| `bank.db` | SQLite database (auto-created on first run) |

## How to Use

When you run `bank.py` you'll see a menu:

```
=============================
     ELITE 102 BANK APP
=============================
1. Create Account
2. Deposit
3. Withdraw
4. Check Balance
5. List All Accounts
6. Transaction History
7. Wire Transfer
8. Exit
=============================
```

Just type the number and hit Enter. Follow the prompts.

## Database Tables

**accounts** - stores account holder name and balance

**transactions** - logs every deposit, withdrawal, and transfer with a timestamp
