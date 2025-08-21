import os
from typing import List, Tuple

def load_accounts_from_file(file_path: str = "accounts.txt") -> List[Tuple[str, float]]:
    accounts = []
    
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Using default accounts.")
        return [
            ("123456", 1000.0),
            ("789012", 2500.0),
            ("345678", 500.0)
        ]
    
    try:
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                try:
                    if ',' in line:
                        account_number, balance = line.split(',', 1)
                    else:
                        parts = line.split()
                        if len(parts) != 2:
                            print(f"Warning: Invalid format on line {line_num}: {line}")
                            continue
                        account_number, balance = parts
                    
                    account_number = account_number.strip()
                    balance = float(balance.strip())
                    
                    if balance < 0:
                        print(f"Warning: Negative balance on line {line_num}, skipping: {line}")
                        continue
                    
                    accounts.append((account_number, balance))
                    
                except ValueError as e:
                    print(f"Warning: Invalid data on line {line_num}: {line} - {e}")
                    continue
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        print("Using default accounts instead.")
        return [
            ("123456", 1000.0),
            ("789012", 2500.0),
            ("345678", 500.0)
        ]
    
    if not accounts:
        print("No valid accounts found in file. Using default accounts.")
        return [
            ("123456", 1000.0),
            ("789012", 2500.0),
            ("345678", 500.0)
        ]
    
    print(f"Loaded {len(accounts)} accounts from {file_path}")
    return accounts