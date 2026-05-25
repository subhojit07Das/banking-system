from app.core.account import Account

class Bank:
    def __init__(self):
        self.accounts = {}

    def create_account(self, owner, initial_balance, pin):
        acc = Account(owner, initial_balance, pin)
        self.accounts[acc.id] = acc
        return acc;

    def get_account(self, account_id):
        if account_id in self.accounts:
            return self.accounts[account_id]
        return "Account not found"
    
    def close_account(self, account_id, pin):
        if account_id not in self.accounts:
            return "Account no found"
        acc = self.accounts[account_id]
        if acc.verify_pin(pin):
            if acc.balance > 0:
                return "Withdraw remaining amount first"
            if acc.balance == 0:
                del self.accounts[account_id]
                return "Account closed successfully"
        else:
            return "Wrong pin"
        
    def transfer(self, sender_id, receiver_id, amount, pin):
        if sender_id not in self.accounts:
            return "Sender account not found"

        if receiver_id not in self.accounts:
            return "Receiver account not found"
        
        sender = self.accounts[sender_id]
        receiver = self.accounts[receiver_id]

        if not sender.verify_pin(pin):
            return "Wrong pin"
        
        if amount <= 0:
            return "Amount must be greater than zero"
        
        if amount > sender.balance:
            return "Insufficient balance"

        sender.balance -= amount
        receiver.balance += amount

        sender.history.append({"type": "transfer", "from": f"{sender_id}", "amount": amount, "to": f"{receiver_id}", "balance_after": sender.balance})

        receiver.history.append({"type": "transfer_received", "from": f"{sender_id}", "amount": amount, "balance_after": receiver.balance})

        return "Transfer Successful"

    def list_account(self):
        return self.accounts.values()