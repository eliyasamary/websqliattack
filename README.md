# websqliattack

**websqliattack** is an automated tool designed to detect SQL injection vulnerabilities in web applications.  
It was developed as part of a software security project and includes both offensive and defensive demonstrations.

## Features

- 🔍 **Intelligent Scraping**: Crawls websites to identify forms and input fields.  
- 💉 **SQL Injection Detection**: Performs both non-blind and blind SQL injection attacks.  
- 🛡️ **Demo Applications**: Includes a vulnerable backend for practice and a protected backend to demonstrate secure coding techniques.  
- 🎯 **Attack Orchestrator**: Automates the scanning, scraping, and attack execution process.  
- 📜 **Logging System**: Records all findings and attack results for later analysis.  

## Structure

- `pre-protecting/`: Vulnerable backend application (Node.js + MySQL).  
- `post-protecting/`: Secured backend application with input validation and parameterized queries.  
- `py-prod/`: Python modules for orchestrating attacks, scraping, and payload generation.  
- `tutorial/`: Documentation and explanations (see [Tutorial PDF](./Tutorial_websqliattack.pdf)).  

## Installation

```bash
git clone https://github.com/eliyasamary/websqliattack
cd websqliattack
```

Install dependencies:

```bash
pip install -r requirements.txt
npm install   # For the Node.js backend examples
```

## Usage

### Run the vulnerable backend

```bash
cd pre-protecting/back
node index.js
```

### Run the protected backend

```bash
cd post-protecting/back
node index.js
```

### Launch attack orchestrator

```bash
cd py-prod
python main.py
```

The orchestrator will:
1. Detect the target website type (React vs. non-React).  
2. Scrape for input forms.  
3. Launch SQL injection attacks.  
4. Log results into a report file.  

## Example Workflow

1. Start the vulnerable backend (`pre-protecting/back`).  
2. Run the attack orchestrator (`py-prod/main.py`) against it.  
3. Review the generated log file for discovered vulnerabilities.  
4. Start the protected backend (`post-protecting/back`) and observe the difference.  

## Tutorial

A full tutorial with step-by-step explanations is available here:  
[📘 Tutorial - websqliattack](./Tutorial_websqliattack.pdf)

## Disclaimer ⚠️

This tool is intended **for educational purposes only**.  
Do not use it on systems you do not own or do not have explicit permission to test. Unauthorized use may be illegal.  

---

Developed as part of a **Compilation & Security course project** in a B.Sc. in Software Engineering.
