from dotenv import load_dotenv
from app.core.bank import create_account, get_account, get_history, deposit, withdraw, transfer, verify_pin, close_account
from app.core.database import get_db, engine
from sqlalchemy.orm import Session
from app.core.auth import create_access_token, verify_token
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from app.core.models import Base
import os

load_dotenv()
app = FastAPI()
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/login")
def login_page():
    return FileResponse("app/static/login.html")

@app.get("/")
def root():
    return RedirectResponse(url="/login")

@app.get("/ui")
def ui():
    return FileResponse("app/static/index.html")

@app.get("/register")
def register_page():
    return FileResponse("app/static/register.html")

@app.post("/login")
def login(account_id: str, pin: str, db: Session = Depends(get_db)):
    account = get_account(db, account_id)
    if not account:
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    
    if not verify_pin(pin, account.pin):
        return JSONResponse(status_code=401, content={"error": "Incorrect Pin"})

    token = create_access_token({"account_id": account.id})

    return {"access_token": token, "token_type": "bearer"}

@app.post("/accounts")
def createAccount(owner: str, balance: float, pin: str, db: Session = Depends(get_db)):
    if balance < 0:
        return JSONResponse(status_code=400, content={"error": "Initial balance cannot be negative"})
    acc = create_account(db, owner, balance, pin)
    return {"id": acc.id, "owner": acc.owner, "balance": acc.balance}

@app.get("/accounts/{account_id}")
def getAccount(account_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = get_account(db, account_id)
    if acc is None:
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    
    return {"id": acc.id, "owner": acc.owner, "balance": acc.balance}

@app.post("/accounts/{account_id}/deposit")
def deposits(account_id: str, amount: float, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = get_account(db, account_id)
    if acc is None:
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    
    message = deposit(db , acc, amount)
    if message != "Deposit successful":
        return JSONResponse(status_code=400, content={"error": "Amount must be greater than zero"})
    
    return {"message": message, "balance": acc.balance}

@app.post("/accounts/{account_id}/withdraw")
def withdraws(account_id: str, amount: float, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = get_account(db, account_id)
    if acc is None:
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    
    message = withdraw(db , acc, amount)
    if message == "Amount should be greater than 0":
        return JSONResponse(status_code=400, content={"error": message})
    
    if message == "Insufficient balance":
        return JSONResponse(status_code=400, content={"error": message})
    
    return {"message": message, "balance": acc.balance}

@app.get("/accounts/{account_id}/history")
def history(account_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = get_account(db, account_id)
    if acc is None:
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    
    result = get_history(acc)
    return {"history": result}

@app.delete("/accounts/{account_id}")
def accountDelete(account_id: str, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None:
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = get_account(db, account_id)
    if acc is None:
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    
    message = close_account(db, acc)
    if message == "Withdraw remaining amount first":
        return JSONResponse(status_code=400, content={"error": "Withdraw remaining amount first"})
    return {"message": message}

@app.post("/accounts/{account_id}/transfer")
def amountTransfer(account_id: str, receiver_id: str, amount: float, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_token(token)
    if payload is None: 
        return JSONResponse(status_code=401, content={"error": "Invalid or expired token"})
    
    if payload["account_id"] != account_id:
        return JSONResponse(status_code=403, content={"error": "Unauthorized"})
    
    acc = get_account(db, account_id)
    if acc is None:
        return JSONResponse(status_code=404, content={"error": "Account not found"})
    
    receiver = get_account(db, receiver_id)
    if receiver is None:
        return JSONResponse(status_code=404, content={"error": "Receiver not found"})
    
    message = transfer(db, acc, receiver, amount)
    if message == "The amount cannot be below 0":
        return JSONResponse(status_code=400, content={"error": "Amount must be greater than zero"})
    if message == "Insufficient balance":
        return JSONResponse(status_code=400, content={"error": "Insufficient balance"})

    return {"message": "Transfer Successful"}