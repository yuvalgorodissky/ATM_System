class Account:
    def __init__(self, account_number, initial_balance=0.0):
        self.account_number = account_number
        self.balance = float(initial_balance)
    
    def get_balance(self):
        return self.balance
    
    def withdraw(self, amount):
        if amount <= 0:
            return False, "Invalid amount: withdrawal amount must be positive"
        
        if amount > self.balance:
            return False, "Insufficient funds"
        
        self.balance -= amount
        return True, f"Successfully withdrew ${amount:.2f}. New balance: ${self.balance:.2f}"
    
    def deposit(self, amount):
        if amount <= 0:
            return False, "Invalid amount: deposit amount must be positive"
        
        self.balance += amount
        return True, f"Successfully deposited ${amount:.2f}. New balance: ${self.balance:.2f}"