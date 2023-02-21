from app.calculations import add,BankAccount,InsufficientFunds
import pytest

@pytest.fixture
def zero_account():
    return BankAccount()

@pytest.fixture
def set_account():
    return BankAccount(100)    

@pytest.mark.parametrize("num1,num2,expected",[(3,4,7),(5,6,11),(9,4,13)])
def test_add(num1,num2,expected):
    assert add(num1,num2) == expected


def test_bank_set_initial_balance(set_account):
    assert set_account.balance == 100


def test_balance_zero_default(zero_account):
    assert zero_account.balance == 0    

def test_bank_deposit(set_account):
    set_account.deposit(20)
    assert set_account.balance == 120

def test_bank_withdraw(set_account):
    set_account.withdraw(40)
    assert set_account.balance == 60

def test_bank_collect_interest(set_account):
    set_account.collect_interest()
    assert round(set_account.balance,5) == 110

@pytest.mark.parametrize("deposited,withdrew,expected",[(200,50,150),(500,250,250),(150,40,110)])
def test_bank_transactions(zero_account,deposited,withdrew,expected):
    zero_account.deposit(deposited)
    zero_account.withdraw(withdrew)
    assert zero_account.balance == expected

def test_insufficient_funds(set_account):
    with pytest.raises(InsufficientFunds):
        set_account.withdraw(200)
