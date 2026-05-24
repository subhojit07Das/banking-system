from fastapi import FastAPI
from app.core.bank import Bank

app = FastAPI()
bank = Bank()

@app.get("/")
def root():
    return {"message": "Banking System is running"}

@app.post("/accounts")
def create_account(owner: str, initial_balance: float):
    acc = bank.create_account(owner, initial_balance)
    return {"id": acc.id, "owner": acc.owner, "balance": acc.balance}

@app.get("/accounts")
def list_accounts():
    accounts = bank.list_account()
    return [{"id": acc.id, "owner": acc.owner, "balance": acc.balance} for acc in accounts]


@app.get("/accounts/{account_id}")
def get_account(account_id: str):
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return {"error": "Account not found"}
    return {"id": acc.id, "owner": acc.owner, "balance": acc.balance}

@app.post("/accounts/{account_id}/deposits")
def deposit(account_id: str, amount: float):
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return {"error": "Account not found"}
    message = acc.deposit(amount)
    return {"message": message, "balance": acc.balance}

@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, amount: float):
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return {"error": "Account not found"}
    message = acc.withdraw(amount)
    return {"message": message, "balance": acc.balance}

@app.get("/accounts/{account_id}/history")
def history(account_id: str):
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return {"error": "Account not found"}
    return {"history": acc.get_history()}