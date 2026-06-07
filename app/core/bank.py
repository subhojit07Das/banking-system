from sqlalchemy.orm import Session
from app.core.models import Account, Transaction
import bcrypt
import uuid

def hash_pin(pin: str) -> str:
    return bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode('utf-8')

def verify_pin(pin: str, hashed: bytes) -> bool:
    return  bcrypt.checkpw(pin.encode(), hashed.encode())

def create_account(db: Session, owner: str, initial_balance: float, pin: str):
    acc_id = "ACC" + str(uuid.uuid4())[:8]
    account = Account (
        id = acc_id,
        owner = owner,
        balance = initial_balance,
        pin = hash_pin(pin),
    )

    db.add(account)
    db.commit()
    db.refresh(account)

    return account

def get_account(db: Session, account_id: str):
    return db.query(Account).filter(Account.id == account_id).first()

def close_account(db: Session, account: Account):
    if account.balance > 0:
        return "Withdraw remaining amount first"
    
    db.delete(account)
    db.commit()
    
    return "Account closed successfully"

def deposit(db: Session, account: Account, amount: float):
    if amount <= 0:
        return "Amount should be greater than 0"
    
    account.balance += amount
    
    gen_id = str(uuid.uuid4()) 
    transaction = Transaction(
        id = gen_id,
        account_id = account.id,
        type = "DEPOSIT",
        amount = amount,
        balance_after = account.balance
    )

    db.add(transaction)
    db.commit()
    db.refresh(account)

    return "Deposit successful"

def withdraw(db: Session, account: Account, amount: float):
    if amount <= 0:
        return "Amount should be greater than 0"
    
    if amount > account.balance:
        return "Insufficient balance"
    

    account.balance -= amount

    transaction = Transaction(
        id = str(uuid.uuid4()),
        account_id = account.id,
        type = "WITHDRAW",
        amount = amount,
        balance_after = account.balance
    )

    db.add(transaction)
    db.commit()
    db.refresh(account)

    return "Withdraw successful"

def transfer(db: Session, sender: Account, receiver: Account, amount: float):
    if amount <= 0:
        return "The amount cannot be below 0"
    
    if sender.balance < amount:
        return "Insufficient balance"
    
    sender.balance -= amount
    receiver.balance += amount

    sender_txn = Transaction (
        id = str(uuid.uuid4()),
        account_id = sender.id,
        type = "TRANSFER",
        amount = amount,
        related_account = receiver.id,
        balance_after = sender.balance
    )

    receiver_txn = Transaction (
        id = str(uuid.uuid4()),
        account_id = receiver.id,
        type = "TRANSFER_RECEIVED",
        amount = amount,
        related_account = sender.id,
        balance_after = receiver.balance
    )

    db.add(sender_txn)
    db.add(receiver_txn)
    db.commit()

    return "Transfer Successful"

def get_history(account: Account):
    return account.transactions