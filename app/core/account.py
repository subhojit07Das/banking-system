class Account:
    counter = 1000 
    def __init__(self, owner, initial_balance):
        Account.counter += 1
        self.id = "ACC" + str(Account.counter)
        self.owner = owner
        self.balance = initial_balance
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            return "Amount must be greater than zero"
        self.balance += amount
        self.history.append({"type": "deposit", "amount": amount, "balance_after": self.balance})
        return "Deposit successful"
    
    def withdraw(self, amount):
        if amount <= 0:
            return "Amount must be greater than zero"
        if self.balance < amount:
            return "Insufficient balance"
        self.balance -= amount
        self.history.append({"type": "withdraw", "amount": amount, "balance_after": self.balance})
        return "Withdrawn Successful"