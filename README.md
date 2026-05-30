# Banking System

A REST API banking system built with Python and FastAPI, featuring JWT authentication, a web UI, Docker containerization, and deployment on AWS EKS.

## Tech Stack

- **Language**: Python 3.13
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Auth**: JWT (JSON Web Tokens) via `python-jose`
- **Frontend**: HTML, CSS, JavaScript
- **Containerization**: Docker
- **Registry**: AWS ECR
- **Orchestration**: Kubernetes (AWS EKS)

## Features

- Register bank accounts with PIN protection
- JWT-based login — authenticate once, use token for all operations
- Deposit and withdraw money
- Transfer money between accounts
- View account details and transaction history
- Close account (balance must be zero)
- PINs hashed with SHA-256 — never stored as plain text
- Token automatically expires after 30 minutes
- Proper HTTP status codes (200, 400, 401, 403, 404)
- Web UI for non-technical users
- Auto page reload after every successful action

## Project Structure

```
banking-system/
├── app/
│   ├── main.py               # FastAPI entry point and all routes
│   ├── core/
│   │   ├── account.py        # Account class — deposit, withdraw, history
│   │   ├── bank.py           # Bank class — manages all accounts
│   │   ├── auth.py           # JWT token creation and verification
│   │   └── __init__.py
│   └── static/
│       ├── index.html        # Main banking UI
│       ├── login.html        # Login page
│       ├── register.html     # Register page
│       ├── app.js            # Main UI JavaScript
│       ├── login.js          # Login logic
│       ├── register.js       # Register logic
│       ├── style.css         # Main styles
│       ├── login.css         # Login styles
│       └── register.css      # Register styles
├── tests/
│   └── test_account.py       # Pytest unit tests
├── k8s/
│   ├── deployment.yaml       # Kubernetes deployment manifest
│   └── service.yaml          # Kubernetes LoadBalancer service
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13
- Docker (optional)
- AWS CLI + kubectl + eksctl (for deployment only)

### Environment Setup

Create a `.env` file in the project root:

```
SECRET_KEY=your_generated_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

> Never commit `.env` to version control — it's already in `.gitignore`.

### Run Locally

```bash
# Clone the repo
git clone https://github.com/subhojit07Das/banking-system.git
cd banking-system

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
PYTHONPATH=. uvicorn app.main:app --reload
```

Visit `http://localhost:8000` — automatically redirects to the login page.

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

### Run with Docker

```bash
# Build the image
docker build -t banking-system .

# Run the container
docker run -p 8000:8000 --env-file .env banking-system
```

## Authentication Flow

```
Register → Get Account ID
    ↓
Login with Account ID + PIN → Receive JWT Token
    ↓
Token stored in localStorage
    ↓
All requests send token in Authorization header
    ↓
Token expires after 30 minutes → Login again
    ↓
Exit / Close Account → Token cleared from localStorage
```

## API Endpoints

### Public Routes (no token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Redirects to `/login` |
| GET | `/login` | Login page |
| GET | `/register` | Register page |
| POST | `/login` | Authenticate and receive JWT token |
| POST | `/accounts` | Create a new account |

### Protected Routes (JWT token required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ui` | Main banking UI |
| GET | `/accounts/{id}` | Get account details |
| POST | `/accounts/{id}/deposit` | Deposit money |
| POST | `/accounts/{id}/withdraw` | Withdraw money |
| POST | `/accounts/{id}/transfer` | Transfer money to another account |
| GET | `/accounts/{id}/history` | View transaction history |
| DELETE | `/accounts/{id}` | Close account (balance must be zero) |

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 400 | Bad request (invalid amount, insufficient funds, balance not zero) |
| 401 | Unauthorized (wrong PIN or invalid/expired token) |
| 403 | Forbidden (token valid but accessing another account) |
| 404 | Account not found |

## API Examples

### Register

```bash
curl -X POST "http://localhost:8000/accounts?owner=Subhojit&initial_balance=1000&pin=1234"
```

```json
{
  "id": "ACC1001",
  "owner": "Subhojit",
  "balance": 1000.0
}
```

### Login

```bash
curl -X POST "http://localhost:8000/login?account_id=ACC1001&pin=1234"
```

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Deposit (with token)

```bash
curl -X POST "http://localhost:8000/accounts/ACC1001/deposit?amount=500" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9..."
```

```json
{
  "message": "Deposit successful",
  "balance": 1500.0
}
```

### Transfer (with token)

```bash
curl -X POST "http://localhost:8000/accounts/ACC1001/transfer?receiver_id=ACC1002&amount=200" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiJ9..."
```

```json
{
  "message": "Transfer Successful"
}
```

## Security

- PINs hashed with SHA-256 before storage — never stored as plain text
- JWT tokens signed with a secret key stored in `.env`
- Tokens expire after 30 minutes
- Every protected route verifies the token before processing
- Account ownership check — token account ID must match the requested account ID
- Secret key generated with Python's `secrets` module
- `.env` excluded from version control via `.gitignore`

## Running Tests

```bash
pytest tests/ -v
```

Expected output:

```
tests/test_account.py::test_deposit         PASSED
tests/test_account.py::test_withdraw        PASSED
tests/test_account.py::test_overdraft       PASSED
tests/test_account.py::test_invalid_deposit PASSED
4 passed in 0.01s
```

## Deployment

### Push to AWS ECR

```bash
# Authenticate
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.ap-south-1.amazonaws.com

# Tag and push
docker tag banking-system:latest <account-id>.dkr.ecr.ap-south-1.amazonaws.com/banking-system:latest
docker push <account-id>.dkr.ecr.ap-south-1.amazonaws.com/banking-system:latest
```

### Deploy to AWS EKS

```bash
# Connect to cluster
aws eks update-kubeconfig --region ap-south-1 --name banking-system

# Apply manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Get public URL
kubectl get svc banking-svc
```

### Tear Down (avoid AWS charges)

```bash
eksctl delete cluster --name=banking-system --region=ap-south-1
```

## What's Next

- PostgreSQL database (persistent storage)
- CI/CD with GitHub Actions (auto deploy on push)

## Author

Subhojit — built as a learning project covering Python, REST APIs, JWT authentication, Docker, AWS EKS and Kubernetes.