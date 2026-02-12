# AI-Powered Security Guardrail System

A cloud-native architecture designed to integrate Large Language Models (LLMs) into enterprise workflows, ensuring high security, data anonymization, and continuous code quality monitoring.

## 🚀 Project Overview

This system acts as an **intelligent security intermediary** (middleware) between end-users and an AI engine. It is engineered to protect sensitive data and prevent model exploitation through a scalable, microservices-based architecture deployed on AWS.

### Key Features
* **Multi-Layer Guardrails:** Ingress filtering to block Prompt Injection and Egress filtering to prevent data leakage.
* **PII Masking (Data Governance):** Automated anonymization of sensitive information (e.g., IBANs) using advanced regex patterns before data reaches the LLM or returns to the user.
* **AI Context Anchoring:** Advanced system prompting techniques that confine AI behavior to specific business domains (e.g., Transaction Risk Analysis).
* **Automated CI/CD:** A robust pipeline integrated with GitHub Actions for automated testing and static analysis.

---

## 🏗️ Technical Architecture

The project implements a hybrid-cloud strategy to balance security, performance, and cost-efficiency:

1.  **Application Load Balancer (ALB):** Acts as the single entry point, managing traffic distribution and SSL termination.
2.  **Logic Layer (AWS Fargate):** A Dockerized **FastAPI** service that executes security policies, sanitizes data, and manages the API lifecycle.
3.  **Inference Layer (Amazon EC2):** A dedicated instance hosting the **Ollama** engine, running LLMs (e.g., TinyLlama) in a secure, isolated environment.
4.  **Network Security:** Fine-grained AWS Security Groups enforce a "least privilege" communication policy between the Fargate container and the EC2 inference node.



---

## 🛠️ Technology Stack

* **Language:** Python 3.9+
* **API Framework:** FastAPI
* **Infrastructure:** AWS CDK (Infrastructure as Code)
* **Containerization:** Docker
* **AI Engine:** Ollama / TinyLlama
* **Quality & Security:** SonarQube, Pytest
* **CI/CD:** GitHub Actions

---

## 🛡️ Quality Assurance & Security Compliance

The system is built with a "Security by Design" approach, featuring:

* **Static Analysis (SonarQube):** Continuous scanning for vulnerabilities, security hotspots, and technical debt.
* **Dynamic Testing:** Automated unit tests using `pytest` and `requests-mock` to validate guardrails without infrastructure dependencies.
* **Code Coverage:** Integrated quality gates to ensure high test coverage across critical security modules.
* **Red Teaming Resilience:** Hardened against sophisticated attacks including *Persona Adoption*, *Context Switching*, and *Base64-encoded payloads*.



---

## 📋 Setup & Usage

### Prerequisites
* Docker installed locally
* AWS CLI configured with appropriate credentials
* AWS CDK CLI installed (`npm install -g aws-cdk`)

### Local Development
1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/ai-security-guardrail.git](https://github.com/your-username/ai-security-guardrail.git)
    cd ai-security-guardrail
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r app/requirements.txt
    ```
3.  **Run unit tests with coverage report:**
    ```bash
    pytest --cov=app app/tests/ --cov-report=xml
    ```

---

## 📈 Conclusion
This project serves as a blueprint for deploying Generative AI in highly regulated sectors (such as Fintech or Healthtech), where data privacy, auditability, and system stability are paramount requirements.
