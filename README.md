# Simple Blockchain with Flask

A minimal, fully-functional blockchain application built with Python and Flask, featuring a clean web interface, transaction handling, mining, chain validation, and Docker support. Designed for learning, experimentation, and demonstration of core blockchain concepts.

---

## Features

- Block and chain architecture
- Proof-of-Work (PoW) algorithm
- Dynamic transaction management (mempool)
- Mining logic with difficulty control
- Chain validation and tamper detection
- Web interface built with Flask and Jinja2
- Styled frontend (HTML + CSS)
- Dockerized for easy deployment

---

## Project Structure

```
simple-blockchain/
├── blockchain.py              # Main application logic (Flask + blockchain)
├── Dockerfile                 # Docker build file
├── requirements.txt           # Python dependencies
├── templates/                 # Jinja2 HTML templates
│   ├── index.html
│   ├── add_transaction.html
│   └── validate.html
└── static/
    └── css/
        └── styles.css         # Modern frontend styling
```

---

## Getting Started (Local)

### Requirements

- Python 3.8+
- pip (Python package installer)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/simple-blockchain.git
cd simple-blockchain

# Install dependencies
pip install -r requirements.txt

# Run the app
python blockchain.py
```

### Access the App

Visit: [http://localhost:5000](http://localhost:5000)

---

## Usage

### 1. Add a Transaction

- Go to `/add_transaction`
- Submit a transaction (e.g. "Alice pays Bob 5 BTC")

### 2. Mine a Block

- Visit `/mine`
- This collects all pending transactions and mines a new block

### 3. Validate the Chain

- Navigate to `/validate`
- Confirms the chain’s integrity and detects tampering

---

## Docker Deployment

### 1. Build the Docker Image

```bash
docker build -t simple-blockchain .
```

### 2. Run the Container

```bash
docker run -p 5000:5000 simple-blockchain
```

### 3. Access the App

Visit: [http://
