from fastapi import FastAPI
from routers import accounts
from src.models.bank import Bank
from src.config.config_manager import get_server_config, get_environment, print_current_config

app = FastAPI(title="ATM System API", version="1.0.0")

bank = Bank.get_instance()
bank.initialize_accounts("accounts.txt")

app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])

@app.get("/")
def read_root():
    return {
        "message": "ATM System API is running",
        "environment": get_environment()
    }

if __name__ == "__main__":
    import uvicorn
    
    print("Starting ATM System API...")
    print_current_config()
    
    server_config = get_server_config()
    uvicorn.run(
        app,
        host=server_config["host"],
        port=server_config["port"]
    )