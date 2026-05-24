from app.core.account import Account

def test_deposit():
    acc = Account("Subhojit", 1000, "1235")
    acc.deposit(500, "1235")
    assert acc.balance == 1500

def test_withdraw():
    acc = Account("Subhojit", 500, "1235")
    acc.withdraw(500, "1235")
    assert acc.balance == 0

def test_overdarft():
    acc = Account("Subhojit", 1000, "1235")
    acc.withdraw(2000, "1235")
    assert acc.balance == 1000

def test_invalid_deposit():
    acc = Account("Subhojit", 1000, "1235")
    acc.deposit(0, "1235")
    assert acc.balance == 1000