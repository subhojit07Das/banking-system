from dotenv import load_dotenv
from app.core.auth import create_access_token, verify_token
from fastapi import FastAPI
from app.core.bank import Bank
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import os

load_dotenv()
app = FastAPI()
bank = Bank()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/login")
def login_page():
    return FileResponse("app/static/login.html")

@app.get("/")
def root():
    return RedirectResponse(url="/login")

@app.get("/ui")
def ui(token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        return FileResponse(url="/login")
    return FileResponse("app/static/index.html")

@app.get("/register")
def register_page():
    return FileResponse("app/static/register.html")

@app.post("/login")
def login(account_id: str, pin: str):
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    if not acc.verify_pin(pin):
        return JSONResponse(status_code=401, content={"error": "Wrong pin"})
    token = create_access_token({"account_id": acc.id})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/accounts")
def create_account(owner: str, initial_balance: float, pin: str):
    if initial_balance < 0:
        return JSONResponse(status_code=400, content={"error": "Initial balance cannot be negative"})
    acc = bank.create_account(owner, initial_balance, pin)
    return {"id": acc.id, "owner": acc.owner, "balance": acc.balance}

@app.get("/accounts/{account_id}")
def get_account(account_id: str, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    return {"id": acc.id, "owner": acc.owner, "balance": acc.balance}

@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, amount: float, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    message = acc.deposit(amount)
    if message == "Amount must be greater than zero":
        return JSONResponse(status_code=400, content={"error": "Amount must be greater than zero"})
    return {"message": message, "balance": acc.balance}

@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, amount: float, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    message = acc.withdraw(amount)
    if message == "Amount must be greater than zero":
        return JSONResponse(status_code=400, content={"error": "Amount must be greater than zero"})   
    if message == "Insufficient balance":
        return JSONResponse(status_code=400, content={"error": "Insufficient Balance"})
    return {"message": message, "balance": acc.balance}

@app.get("/accounts/{account_id}/history")
def history(account_id: str, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    
    result = acc.get_history()
    return {"history": result}

@app.delete("/accounts/{account_id}")
def close_account(account_id: str, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = bank.get_account(account_id)
    if acc == "Account not found":
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    message = bank.close_account(account_id)
    if message == "Withdraw remaining amount first":
        return JSONResponse(status_code=400, content={"error": "Withdraw remaining amount first"})
    return {"message": message}

@app.post("/accounts/{account_id}/transfer")
def transfer_money(account_id: str, receiver_id: str, amount: float, token: str = Depends(oauth2_scheme)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    message = bank.transfer(account_id, receiver_id, amount)
    if message == "Sender account not found":
        return JSONResponse(status_code=404, content={"error": "Sender account not found"})
    if message == "Receiver account not found":
        return JSONResponse(status_code=404, content={"error": "Receiver account not found"})
    if message == "Amount must be greater than zero":
        return JSONResponse(status_code=400, content={"error": "Amount must be greater than zero"})
    if message == "Insufficient balance":
        return JSONResponse(status_code=400, content={"error": "Insufficient balance"})
    return {"message": "Transfer Successful"}