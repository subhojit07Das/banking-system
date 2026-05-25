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
    
    def list_account(self):
        return self.accounts.values()