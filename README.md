# ATM System API

A comprehensive ATM (Automated Teller Machine) system built with FastAPI, implementing secure account management with balance inquiry, withdrawal, and deposit functionalities.

## Live Demo

- **Repository**: [https://github.com/yuvalgorodissky/ATM_System](https://github.com/yuvalgorodissky/ATM_System)
- **Production API**: `http://56.228.41.210:8000`
- **API Documentation**: `http://56.228.41.210:8000/docs`

## Table of Contents

- [Features](#features)
- [Architecture & Design Decisions](#architecture--design-decisions)
- [Installation & Setup](#installation--setup)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Challenges & Solutions](#challenges--solutions)
- [Project Structure](#project-structure)
- [Contributing](#contributing)

## Features

- **Account Management**: Create and manage bank accounts with unique account numbers
- **Balance Inquiry**: Real-time balance checking with thread-safe operations
- **Money Withdrawal**: Secure withdrawal with insufficient funds validation
- **Money Deposit**: Deposit functionality with amount validation
- **Thread Safety**: Concurrent request handling with proper locking mechanisms
- **Configuration Management**: Environment-based configuration (development/production)
- **File-Based Initialization**: Account loading from external text files
- **Input Validation**: Comprehensive validation using Pydantic models
- **Error Handling**: Proper HTTP status codes and descriptive error messages

## Architecture & Design Decisions

### Core Design Patterns

#### 1. Singleton Pattern for Bank Management
- **Decision**: Implemented Bank as a singleton to ensure single source of truth
- **Rationale**: Prevents multiple bank instances and ensures data consistency
- **Implementation**: Thread-safe singleton with double-checked locking

```python
class Bank:
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Bank, cls).__new__(cls)
        return cls._instance
```

#### 2. Account-Level Thread Safety
- **Decision**: Individual locks for each account rather than global locking
- **Rationale**: Allows concurrent operations on different accounts while ensuring account-specific thread safety
- **Implementation**: Each Account instance has its own `threading.Lock()`

#### 3. In-Memory Data Storage
- **Decision**: Dictionary-based storage instead of database
- **Rationale**: Meets assignment requirements for in-memory storage and simplifies deployment
- **Trade-offs**: Data doesn't persist between restarts (acceptable for demo purposes)

#### 4. Router-Based API Architecture
- **Decision**: Separated concerns using FastAPI routers
- **Rationale**: Modular code organization and easier maintenance
- **Structure**: 
  - `main.py`: Application setup and configuration
  - `routers/accounts.py`: Account-specific endpoints

#### 5. Configuration Management System
- **Decision**: YAML-based configuration with environment variable overrides
- **Rationale**: Easy deployment across different environments
- **Flexibility**: Supports development, testing, and production configurations

### Data Models

#### Account Model
```python
class Account:
    def __init__(self, account_number, initial_balance=0.0):
        self.account_number = account_number
        self.balance = float(initial_balance)
        self._lock = threading.Lock()  # Thread safety
```

#### API Models (Pydantic)
- `BalanceResponse`: Account balance information
- `WithdrawRequest`/`DepositRequest`: Transaction request models
- `TransactionResponse`: Transaction result with updated balance

## Access the Production API

The ATM System is deployed on AWS EC2 instance and ready to use:

- **Production API**: `http://56.228.41.210:8000`
- **Interactive Documentation**: `http://56.228.41.210:8000/docs`
- **Alternative Documentation**: `http://56.228.41.210:8000/redoc`
- **Hosting**: AWS EC2 Instance

No installation required - the API is live and accessible immediately.

## API Endpoints

### Base URL
- **Production**: `http://56.228.41.210:8000`

### Available Endpoints

#### 1. System Status
```http
GET /
```
**Response:**
```json
{
  "message": "ATM System API is running",
  "environment": "development"
}
```

#### 2. Get Account Balance
```http
GET /accounts/{account_number}/balance
```

**Parameters:**
- `account_number` (path): The account number to check

**Response:**
```json
{
  "account_number": "123456",
  "balance": 1000.0
}
```

**Error Responses:**
- `404`: Account not found

#### 3. Withdraw Money
```http
POST /accounts/{account_number}/withdraw
```

**Parameters:**
- `account_number` (path): The account number
- Request body:
```json
{
  "amount": 100.0
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully withdrew $100.00. New balance: $900.00",
  "account_number": "123456",
  "balance": 900.0
}
```

**Error Responses:**
- `400`: Insufficient funds or invalid amount
- `404`: Account not found

#### 4. Deposit Money
```http
POST /accounts/{account_number}/deposit
```

**Parameters:**
- `account_number` (path): The account number
- Request body:
```json
{
  "amount": 200.0
}
```

**Response:**
```json
{
  "success": true,
  "message": "Successfully deposited $200.00. New balance: $1100.00",
  "account_number": "123456",
  "balance": 1100.0
}
```

**Error Responses:**
- `400`: Invalid amount (negative or zero)
- `404`: Account not found

## Usage Examples

## Accounts

### Pre-configured Accounts
The system comes with 3 pre-configured accounts:

#### Account 1
- **Account Number**: `123456`
- **Initial Balance**: $1,000.00

#### Account 2
- **Account Number**: `789012`
- **Initial Balance**: $2,500.00

#### Account 3
- **Account Number**: `345678`
- **Initial Balance**: $500.00

### System Assumptions
- **Fixed Account Base**: Current implementation supports these 3 accounts only
- **Account-Centric**: Operations focus on account numbers
- **Simple Structure**: Each account operates independently

### Future Expandability
While the current implementation focuses on account operations with pre-configured accounts, the system can be easily expanded to include:
- User registration and management endpoints
- Multiple accounts per user
- User authentication and authorization
- User profile management
- Account creation workflows

The modular architecture supports these enhancements without major restructuring.

### Using cURL

#### Check Balance
```bash
curl -X GET "http://56.228.41.210:8000/accounts/123456/balance"
```

#### Deposit Money
```bash
curl -X POST "http://56.228.41.210:8000/accounts/123456/deposit" \
  -H "Content-Type: application/json" \
  -d '{"amount": 250.0}'
```

#### Withdraw Money
```bash
curl -X POST "http://56.228.41.210:8000/accounts/123456/withdraw" \
  -H "Content-Type: application/json" \
  -d '{"amount": 100.0}'
```

### Using Python Requests

```python
import requests

base_url = "http://56.228.41.210:8000"

# Check balance for Account 1
response = requests.get(f"{base_url}/accounts/123456/balance")
print(response.json())

# Deposit money to Account 2
response = requests.post(
    f"{base_url}/accounts/789012/deposit",
    json={"amount": 250.0}
)
print(response.json())

# Withdraw money from Account 3
response = requests.post(
    f"{base_url}/accounts/345678/withdraw",
    json={"amount": 100.0}
)
print(response.json())
```

### Using Interactive Documentation

Visit the production API documentation at `http://56.228.41.210:8000/docs` for interactive testing with a web interface.

## Configuration

### Environment Configuration

The system supports multiple environments through `config/config.yaml`:

```yaml
development:
  server:
    host: "127.0.0.1"
    port: 8000
    base_url: "http://localhost:8000"

production:
  server:
    host: "0.0.0.0"
    port: 8000
    base_url: "http://56.228.41.210:8000"
```

### Environment Variables

Override configuration using environment variables:

- `ATM_ENV`: Environment name (development/production)
- `ATM_HOST`: Server host address
- `ATM_PORT`: Server port
- `ATM_BASE_URL`: Custom base URL

### Account Initialization

Accounts are loaded from `accounts.txt`:

```
# ATM System Account Data
# Format: account_number,initial_balance

123456,1000.0
789012,2500.0  
345678,500.0
```

## Challenges & Solutions

### 1. Thread Safety Challenge
**Challenge**: Concurrent requests could cause race conditions when accessing the same account.

**Solution**: Implemented account-level locking with `threading.Lock()` for each account instance.

**Benefits**:
- Prevents race conditions
- Allows concurrent access to different accounts
- Maintains data consistency

### 2. Circular Import Issue
**Challenge**: Router needed to access Bank instance, creating circular imports between `main.py` and `routers/accounts.py`.

**Solution**: Implemented singleton pattern allowing global access to Bank instance without circular dependencies.

**Implementation**:
```python
# In routers/accounts.py
def get_balance(account_number: str):
    bank = Bank.get_instance()  # Access singleton directly
    # ... rest of the logic
```

### 3. Configuration Management
**Challenge**: Supporting multiple deployment environments (development, production) with different settings.

**Solution**: Created flexible YAML-based configuration system with environment variable overrides.

**Benefits**:
- Easy deployment across environments
- No code changes needed for different environments
- Environment variable support for containerized deployments

### 4. Data Persistence
**Challenge**: Assignment required in-memory storage, but needed initial account data.

**Solution**: File-based account initialization that loads data at startup while maintaining in-memory operations.

**Trade-offs**:
- Data doesn't persist between restarts
- Acceptable for demo/assignment purposes
- Could be easily extended to database storage

### 5. API Design Consistency
**Challenge**: Ensuring consistent response formats and error handling across all endpoints.

**Solution**: Used Pydantic models for request/response validation and standardized error handling patterns.

**Benefits**:
- Automatic input validation
- Consistent API responses
- Clear error messages with appropriate HTTP status codes

## Project Structure

```
ATM_System/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── accounts.txt             # Initial account data
├── main.py                  # FastAPI application entry point
├── config/
│   ├── config.yaml         # Environment configurations
│   └── settings.py         # Configuration loading logic
├── src/
│   ├── config/
│   │   └── config_manager.py  # Configuration management
│   ├── models/
│   │   ├── account.py      # Account model with thread safety
│   │   └── bank.py         # Bank singleton implementation
│   └── utils/
│       └── file_loader.py  # Account data file loading
└── routers/
    └── accounts.py         # Account API endpoints
```

## Security Considerations

- **Input Validation**: All inputs validated using Pydantic models
- **Thread Safety**: Account operations are thread-safe
- **Error Handling**: Secure error messages without sensitive information
- **Account Validation**: Proper account existence checking
- **Amount Validation**: Prevents negative amounts and insufficient funds

## Deployment

### Local Deployment
```bash
python main.py
```

### Production Deployment (AWS EC2)
```bash
# Set environment variables
export ATM_ENV=production
export ATM_HOST=0.0.0.0
export ATM_PORT=8000

# Run with uvicorn on AWS EC2 instance
uvicorn main:app --host 0.0.0.0 --port 8000
```



## License

This project is created for educational/assignment purposes.

## Author

**Yuval Gorodissky**
- GitHub: [@yuvalgorodissky](https://github.com/yuvalgorodissky)
- Repository: [ATM_System](https://github.com/yuvalgorodissky/ATM_System)

---

## Support

For questions or issues, please:
1. Check the [API documentation](http://56.228.41.210:8000/docs)
2. Review this README
3. Open an issue on GitHub

---

*This ATM System API was designed and implemented as a comprehensive solution demonstrating modern API development practices with Python and FastAPI.*