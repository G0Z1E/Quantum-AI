Here’s a clean, **student-friendly but professional README.md** you can drop straight into the repo.

---

# Quantum AI Engine

## Overview

Quantum AI is a modular Python-based automation framework designed to simulate an intelligent system that can run multiple tasks, learn from memory, recover from failures, and expand through plug-in “skills.”
It is **not quantum computing**, but rather a *quantum-inspired* architecture focused on adaptability, automation, and scalability.

This project demonstrates:

* Security automation
* AI-style task orchestration
* Modular system design
* Defensive and ethical use of tools

---

## Features

* **Modular Skill System** – Add or remove skills without changing the core engine
* **Supervisor (Self-Healing)** – Detects task failures and triggers recovery logic
* **Persistent Memory** – Saves state and results between runs
* **Task Scheduler** – Runs recurring background jobs
* **CLI Interface** – Easy command-line usage
* **Expandable Architecture** – Ready for AI, trading, voice, or security extensions

---

## Project Structure

```
quantum_ai/
│
├── app.py                  # Main CLI entry point
├── config.py               # Application configuration
│
├── core/
│   ├── engine.py           # Main AI engine
│   ├── memory.py           # Persistent memory store
│   ├── supervisor.py       # Self-healing task supervisor
│   └── tasks.py            # Scheduled task definitions
│
├── skills/
│   ├── base.py             # Skill interface
│   ├── threat_scan.py      # Defensive Nmap scanning skill
│   └── market_watch.py     # Market monitoring (stub)
│
├── utils/
│   └── log.py              # Logging setup
│
└── README.md
```

---

## Requirements

* Python **3.10+**
* Linux or macOS recommended
* Nmap (only if using the threat scan skill)

Install Nmap (Ubuntu):

```bash
sudo apt install nmap
```

---

## Installation

Clone the repository and navigate into it:

```bash
git clone https://github.com/G0Z1E/quantum_ai.git
cd quantum_ai
```

(Optional but recommended)

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Usage

### List Available Skills

```bash
python3 -m quantum_ai.app skills
```

### Run a Skill Once

```bash
python3 -m quantum_ai.app run --skill market_watch
```

### Authorized Defensive Nmap Scan

```bash
python3 -m quantum_ai.app run \
  --skill threat_scan \
  --ctx '{"targets":["192.168.40.130"]}'
```

⚠️ **Only scan systems you own or have permission to test.**

---

### Run Supervisor Loop (Automation Mode)

```bash
python3 -m quantum_ai.app loop
```

Run one cycle only:

```bash
python3 -m quantum_ai.app loop --once
```

---

## Memory System

Quantum AI stores results in a persistent memory file:

```
.quantum_data/memory.json
```

This allows the engine to:

* Remember last task outputs
* Track recovery events
* Maintain state between runs

---

## Self-Healing Supervisor

If a task fails multiple times:

* The supervisor detects the failure
* Triggers a **self-healing routine**
* Resets the task failure counter

This simulates real-world resilient AI systems.

---

## Ethical Use Statement

This project is designed for:

* Defensive security automation
* Education and research
* Ethical system monitoring

**It must not be used for unauthorized scanning, exploitation, or malicious activity.**

---

## Future Enhancements

* AI-driven threat intelligence ingestion
* Trading & financial automation modules
* Voice assistant integration (Temi)
* Docker deployment
* Dashboard UI
* Secure API layer

---

## Author

**Ikenna Uba**
Cybersecurity • Automation • AI Systems

---


