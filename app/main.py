from fastapi import FastAPI
from app.core.bank import Bank
from fastapi.responses import JSONResponse

app = FastAPI()
bank = Bank()

@app.get("/")
def root():
    return {"message": "Banking System is running"}

@app.post("/accounts")
def create_account(owner: str, initial_balance: float, pin: str):
    acc = bank.create_account(owner, initial_balance, pin)
    return {"id": acc.id, "owner": acc.owner, "balance": acc.balance}

@app.get("/accounts/{account_id}")
def get_account(account_id: str, pin: str):
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    if not acc.verify_pin(pin):
        return JSONResponse(status_code=401, content={"error": "Wrong pin"})
    return {"id": acc.id, "owner": acc.owner, "balance": acc.balance}

@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, amount: float, pin: str):
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    message = acc.deposit(amount, pin)
    if message == "Wrong Pin":
        return JSONResponse(status_code=401, content={"error": "Wrong pin"})
    if message == "Amount must be greater than zero":
        return JSONResponse(status_code=400, content={"error": "Amount must be greater than zero"})
    return {"message": message, "balance": acc.balance}

@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, amount: float, pin: str):
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    message = acc.withdraw(amount, pin)
    if message == "Wrong Pin":
        return JSONResponse(status_code=401, content={"error": "Wrong pin"})
    if message == "Amount must be greater than zero":
        return JSONResponse(status_code=400, content={"error": "Amount must be greater than zero"})   
    if message == "Insufficient Balance":
        return JSONResponse(status_code=400, content={"error": "Insufficient Balance"})
    return {"message": message, "balance": acc.balance}

@app.get("/accounts/{account_id}/history")
def history(account_id: str, pin: str):
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    result = acc.get_history(pin)
    if result == "Wrong Pin":
        return JSONResponse(status_code=401, content={"error": "Wrong Pin"})
    return {"history": result}