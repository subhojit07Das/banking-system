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
    
    def list_account(self):
        return self.accounts.values()