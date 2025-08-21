from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.models.bank import Bank

router = APIRouter()

class WithdrawRequest(BaseModel):
    amount: float

class DepositRequest(BaseModel):
    amount: float

class BalanceResponse(BaseModel):
    account_number: str
    balance: float

class TransactionResponse(BaseModel):
    success: bool
    message: str
    account_number: str
    balance: float

@router.get("/{account_number}/balance", response_model=BalanceResponse)
def get_balance(account_number: str):
    bank = Bank.get_instance()
    account, message = bank.get_account(account_number)
    if account is None:
        raise HTTPException(status_code=404, detail=f"Account {account_number} not found")
    
    return BalanceResponse(
        account_number=account_number,
        balance=account.get_balance()
    )

@router.post("/{account_number}/withdraw", response_model=TransactionResponse)
def withdraw_money(account_number: str, request: WithdrawRequest):
    bank = Bank.get_instance()
    account, message = bank.get_account(account_number)
    if account is None:
        raise HTTPException(status_code=404, detail=f"Account {account_number} not found")
    
    success, message = account.withdraw(request.amount)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return TransactionResponse(
        success=success,
        message=message,
        account_number=account_number,
        balance=account.get_balance()
    )

@router.post("/{account_number}/deposit", response_model=TransactionResponse)
def deposit_money(account_number: str, request: DepositRequest):
    bank = Bank.get_instance()
    account, message = bank.get_account(account_number)
    if account is None:
        raise HTTPException(status_code=404, detail=f"Account {account_number} not found")
    
    success, message = account.deposit(request.amount)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return TransactionResponse(
        success=success,
        message=message,
        account_number=account_number,
        balance=account.get_balance()
    )