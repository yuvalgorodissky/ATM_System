from .account import Account
import threading

class Bank:
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    def __new__(cls):
        """Ensure only one instance exists (Singleton pattern)"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Bank, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize only once"""
        if not Bank._initialized:
            with Bank._lock:
                if not Bank._initialized:
                    self.accounts = {}
                    Bank._initialized = True
    
    @classmethod
    def get_instance(cls):
        """Get the singleton instance of Bank"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def initialize_accounts(self, accounts_file="accounts.txt"):
        """Initialize accounts from file - called only once"""
        if self.accounts:
            return
            
        from ..utils.file_loader import load_accounts_from_file
        
        account_data = load_accounts_from_file(accounts_file)
        for account_number, balance in account_data:
            success, message = self.create_account(account_number, balance)
            if success:
                print(f"Created account {account_number} with balance ${balance:.2f}")
            else:
                print(f"Failed to create account {account_number}: {message}")
    
    def create_account(self, account_number, initial_balance=0.0):
        if account_number in self.accounts:
            return False, f"Account {account_number} already exists"
        
        if initial_balance < 0:
            return False, "Initial balance cannot be negative"
        
        new_account = Account(account_number, initial_balance)
        self.accounts[account_number] = new_account
        return True, f"Account {account_number} created successfully with balance ${initial_balance:.2f}"
    
    def get_account(self, account_number):
        if account_number not in self.accounts:
            return None, f"Account {account_number} not found"
        
        return self.accounts[account_number], "Account found"
    
    def account_exists(self, account_number):
        return account_number in self.accounts
    
    def get_all_accounts(self):
        return list(self.accounts.keys())
    
    def reset_for_testing(self):
        """Reset bank state for testing - use with caution"""
        with self._lock:
            self.accounts.clear()
            print("Bank state reset for testing")
    
    def reload_accounts(self, accounts_file="accounts.txt"):
        """Reload accounts from file - useful for testing"""
        self.reset_for_testing()
        self.initialize_accounts(accounts_file)