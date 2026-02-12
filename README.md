# AI-Powered Security Guardrail System 🛡️

A cloud-native architecture designed to integrate Large Language Models (LLMs) into enterprise workflows, ensuring high security, data anonymization, and continuous code quality monitoring.

## 🚀 Project Overview

This system acts as an **intelligent security intermediary** (middleware) between end-users and an AI engine. It protects sensitive data and prevents model exploitation through a scalable, microservices-based architecture deployed on AWS.

### Key Features

* **Multi-Layer Guardrails:** Ingress filtering to block Prompt Injection and Egress filtering to prevent data leakage (Dual-Layer Sanitization).
* **PII Masking (Data Governance):** Automated anonymization of sensitive information (e.g., IBANs) using advanced regex patterns.
* **AI Context Anchoring:** Advanced system prompting techniques that confine AI behavior to specific business domains (e.g., Transaction Risk Analysis).
* **Automated CI/CD:** A robust pipeline integrated with GitHub Actions for automated testing and static analysis via SonarQube.

---

## 🏗️ Technical Architecture

The project implements a hybrid-cloud strategy to balance security and performance:

1. **Application Load Balancer (ALB):** Single entry point for traffic management and SSL termination.
2. **Logic Layer (AWS Fargate):** Dockerized **FastAPI** service executing security policies and PII masking.
3. **Inference Layer (Amazon EC2):** Dedicated instance hosting the **Ollama** engine and the **TinyLlama** model.
4. **Network Security:** Fine-grained Security Groups enforcing a "least privilege" policy between Fargate and EC2.

```
┌─────────────────────────────────────────────────────────────┐
│                     Internet Gateway                         │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ Application Load     │
              │ Balancer (ALB)       │
              │ - SSL Termination    │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   AWS Fargate        │
              │   (FastAPI Service)  │
              │ - Ingress Filtering  │
              │ - PII Masking        │
              │ - Egress Filtering   │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Amazon EC2         │
              │   (Ollama + Model)   │
              │ - TinyLlama          │
              │ - Isolated Network   │
              └──────────────────────┘
```

---

## 🛠️ Detailed Deployment Guide

### Prerequisites

- AWS Account with appropriate permissions
- Docker installed locally
- Python 3.9+
- AWS CLI configured
- GitHub account for CI/CD

### 1. AI Inference Layer (Ollama on EC2)

Launch a dedicated EC2 instance (Ubuntu 22.04 LTS, recommended `t3.medium`) and execute:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Configure Ollama to listen on all interfaces for Fargate communication
sudo mkdir -p /etc/systemd/system/ollama.service.d
echo '[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"' | sudo tee /etc/systemd/system/ollama.service.d/override.conf

# Reload and restart service
sudo systemctl daemon-reload
sudo systemctl restart ollama

# Pre-load the model
ollama run tinyllama
```

**Security Group Configuration:**
- Allow inbound traffic on port `11434` from Fargate security group only
- Allow outbound traffic to VPC CIDR

### 2. Quality & Governance Layer (SonarQube on EC2)

Launch an EC2 instance (min 4GB RAM) and deploy via Docker:

```bash
# Install Docker
sudo apt-get update && sudo apt-get install -y docker.io
sudo systemctl start docker && sudo systemctl enable docker

# Optimize system limits for Elasticsearch (required by SonarQube)
sudo sysctl -w vm.max_map_count=262144
sudo sysctl -w fs.file-max=65536

# Run SonarQube Community Build
docker run -d --name sonarqube -p 9000:9000 sonarqube:community
```

**Access SonarQube:**
- Navigate to `http://<EC2_PUBLIC_IP>:9000`
- Default credentials: `admin` / `admin`
- Create a project and generate an authentication token for CI/CD

---

## 🛡️ Quality Assurance & Security Compliance

### Static Analysis (SonarQube)
Continuous scanning for:
- Code vulnerabilities
- Security hotspots
- Technical debt
- Code smells
- Test coverage

### Dynamic Testing
Automated unit tests using:
- `pytest` for test framework
- `requests-mock` to validate guardrails
- Coverage reporting with `pytest-cov`

### Red Teaming Resilience
The system is hardened against:
- **Persona Adoption:** Attempts to make the AI assume unauthorized roles
- **Context Switching:** Efforts to break out of domain constraints
- **Base64-encoded payloads:** Obfuscated injection attempts
- **Jailbreak patterns:** Common prompt injection techniques

---

## 📋 Local Development & CI/CD

### Local Setup

**Clone & Install:**

```bash
git clone https://github.com/your-username/ai-security-guardrail.git
cd ai-security-guardrail
pip install -r app/requirements.txt
```

**Environment Variables:**

Create a `.env` file in the root directory:

```env
OLLAMA_URL=http://localhost:11434
LOG_LEVEL=INFO
ENVIRONMENT=development
```

**Run Tests:**

```bash
pytest app/tests/ --cov=app --cov-report=xml
```

**Run Locally:**

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### CI/CD Pipeline

The included GitHub Action `.github/workflows/ci-cd.yml` automates:

1. **Test Stage:**
   - Python environment setup (3.9)
   - Dependency installation
   - Pytest execution with XML coverage report

2. **Analyze Stage:**
   - SonarQube scanning
   - Quality gate validation
   - Security vulnerability detection

3. **Deploy Stage:**
   - Infrastructure deployment/update via AWS CDK
   - Automatic rollback on failure
   - Blue-green deployment strategy

### GitHub Secrets Configuration

Add the following secrets to your repository:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `SONAR_TOKEN`
- `SONAR_HOST_URL`

---

## 📊 API Documentation

### Endpoints

#### `POST /analyze`

Analyze transaction risk with built-in security guardrails.

**Request:**
```json
{
  "transaction_id": "TXN-12345",
  "amount": 5000.00,
  "account": "IT60X0542811101000000123456",
  "description": "Payment for services"
}
```

**Response:**
```json
{
  "risk_level": "medium",
  "analysis": "Transaction flagged for manual review due to amount threshold",
  "masked_data": {
    "account": "IT60X0542811101***********456"
  }
}
```

#### `GET /health`

Health check endpoint for load balancer.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-02-12T10:30:00Z"
}
```

---

## 🔒 Security Features

### PII Masking Patterns

The system automatically detects and masks:

- **IBANs:** `IT60X0542811101000000123456` → `IT60X0542811101***********456`
- **Credit Cards:** `4532-1234-5678-9010` → `4532-****-****-9010`
- **Email Addresses:** `user@example.com` → `u***@example.com`
- **Phone Numbers:** `+39 123 456 7890` → `+39 *** *** 7890`

### Guardrail Mechanisms

**Ingress Filtering:**
- Pattern matching for known injection techniques
- Content sanitization
- Request validation

**Egress Filtering:**
- Response scanning for leaked PII
- Output validation against business rules
- Anomaly detection

---

## 📈 Monitoring & Observability

### CloudWatch Metrics

- Request latency (p50, p95, p99)
- Error rates
- Guardrail trigger frequency
- Model inference time

### Logging

Structured JSON logging with:
- Request ID correlation
- User context
- Security events
- Performance metrics

---

## 🧪 Testing

### Unit Tests

```bash
pytest app/tests/unit/ -v
```

### Integration Tests

```bash
pytest app/tests/integration/ -v
```

### Security Tests

```bash
pytest app/tests/security/ -v
```

### Test Coverage

Minimum required coverage: **80%**

Current coverage can be viewed in SonarQube or by running:

```bash
pytest --cov=app --cov-report=html
open htmlcov/index.html
```

---

## 🚀 Deployment

### Infrastructure as Code

The project uses AWS CDK for infrastructure provisioning:

```bash
cd infrastructure
npm install
cdk deploy --all
```

### Manual Deployment

1. Build Docker image:
   ```bash
   docker build -t ai-guardrail:latest .
   ```

2. Push to ECR:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
   docker tag ai-guardrail:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-guardrail:latest
   docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/ai-guardrail:latest
   ```

3. Update Fargate service:
   ```bash
   aws ecs update-service --cluster ai-guardrail-cluster --service guardrail-service --force-new-deployment
   ```

---

## 📚 Project Structure

```
ai-security-guardrail/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # Pydantic models
│   ├── services/            # Business logic
│   │   ├── guardrails.py    # Security filtering
│   │   ├── pii_masking.py   # Data anonymization
│   │   └── ollama_client.py # LLM integration
│   ├── tests/               # Test suite
│   │   ├── unit/
│   │   ├── integration/
│   │   └── security/
│   └── requirements.txt     # Python dependencies
├── infrastructure/          # AWS CDK stacks
│   ├── lib/
│   │   ├── network-stack.ts
│   │   ├── compute-stack.ts
│   │   └── security-stack.ts
│   └── cdk.json
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions pipeline
├── Dockerfile               # Container configuration
├── sonar-project.properties # SonarQube configuration
└── README.md                # This file
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards

- Follow PEP 8 for Python code
- Maintain test coverage above 80%
- All tests must pass
- SonarQube quality gate must pass

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Ollama](https://ollama.com/) for local LLM deployment
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [AWS](https://aws.amazon.com/) for cloud infrastructure
- [SonarQube](https://www.sonarqube.org/) for code quality analysis

---

## 📧 Contact

For questions or support, please open an issue or contact the maintainers.

---

## 📖 Additional Resources

- [Architecture Decision Records](docs/adr/)
- [Security Best Practices](docs/security.md)
- [Deployment Guide](docs/deployment.md)
- [Troubleshooting](docs/troubleshooting.md)

---

## 📉 Conclusion

This project serves as a **blueprint for deploying Generative AI in highly regulated sectors** (Fintech/Healthtech), where data privacy, auditability, and system stability are paramount requirements.

By implementing multi-layer security guardrails, automated PII masking, and continuous quality monitoring, this architecture demonstrates how to safely integrate LLMs into production environments without compromising on security or compliance.

**Key Takeaways:**
- Security must be built into every layer, not bolted on
- Automated testing and static analysis are non-negotiable
- PII protection requires both technical controls and process governance
- Cloud-native architectures provide the scalability needed for AI workloads

---

**⭐ If you found this project useful, please consider giving it a star!**
