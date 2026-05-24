# Banking System

A REST API banking system built with Python and FastAPI, containerized with Docker and deployed on AWS EKS.

## Tech Stack

- **Language**: Python 3.13
- **Framework**: FastAPI
- **Server**: Uvicorn
- **Containerization**: Docker
- **Registry**: AWS ECR
- **Orchestration**: Kubernetes (AWS EKS)

## Features

- Create bank accounts with PIN protection
- Deposit and withdraw money (PIN required)
- View transaction history (PIN required)
- Get account details (PIN required)
- All PINs stored as SHA-256 hashes — never plain text

## Project Structure

```
banking-system/
├── app/
│   ├── main.py           # FastAPI entry point and routes
│   └── core/
│       ├── account.py    # Account class with deposit, withdraw, history
│       └── bank.py       # Bank class managing all accounts
├── tests/
│   └── test_account.py   # Pytest unit tests
├── k8s/
│   ├── deployment.yaml   # Kubernetes deployment manifest
│   └── service.yaml      # Kubernetes LoadBalancer service
├── Dockerfile
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.13
- Docker
- AWS CLI (for deployment)
- kubectl + eksctl (for Kubernetes)

### Run Locally

```bash
# Clone the repo
git clone https://github.com/your-username/banking-system.git
cd banking-system

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the server
PYTHONPATH=. uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for the interactive Swagger UI.

### Run with Docker

```bash
# Build the image
docker build -t banking-system .

# Run the container
docker run -p 8000:8000 banking-system
```

## API Endpoints

| Method | Endpoint | Description | PIN Required |
|--------|----------|-------------|--------------|
| POST | `/accounts` | Create a new account | Set at creation |
| GET | `/accounts/{id}` | Get account details | Yes |
| POST | `/accounts/{id}/deposit` | Deposit money | Yes |
| POST | `/accounts/{id}/withdraw` | Withdraw money | Yes |
| GET | `/accounts/{id}/history` | View transaction history | Yes |

### Example: Create Account

```bash
curl -X POST "http://localhost:8000/accounts?owner=Subhojit&initial_balance=1000&pin=1234"
```

Response:
```json
{
  "id": "ACC1001",
  "owner": "Subhojit",
  "balance": 1000.0
}
```

### Example: Deposit

```bash
curl -X POST "http://localhost:8000/accounts/ACC1001/deposit?amount=500&pin=1234"
```

Response:
```json
{
  "message": "Deposit successful",
  "balance": 1500.0
}
```

## Running Tests

```bash
pytest tests/ -v
```

Expected output:
```
tests/test_account.py::test_deposit         PASSED
tests/test_account.py::test_withdraw        PASSED
tests/test_account.py::test_overdarft       PASSED
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

### Tear Down (avoid charges)

```bash
eksctl delete cluster --name=banking-system --region=ap-south-1
```

## Security

- PINs are hashed using SHA-256 before storage
- All sensitive operations require PIN verification
- Account balances are never exposed without a valid PIN
- No plain text credentials stored anywhere

## Author

Subhojit — built as a learning project covering Python, REST APIs, Docker, and AWS EKS.