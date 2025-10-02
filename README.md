# 🤖 AI-Driven Self-Evolving Software

## 📖 Introduction

This repository contains the implementation and experimental code for the paper:

**AI-Driven Self-Evolving Software**

This repository provides:

* ✅ A working implementation of the core algorithm presented in the paper
* ⚙️ Scripts and configuration files to reproduce the reported experiments

---

## 📝 Abstract

Software automation has long been a central goal of software engineering, aiming to **minimize human intervention** in the development lifecycle.
Recent efforts have leveraged **Artificial Intelligence (AI)** to advance software automation with notable progress. However, current AI mainly serves as an **assistant** to human developers, leaving software development still dependent on explicit human input.

This raises a fundamental question:

> *Can AI move beyond its role as an assistant to become a core component of software, enabling genuine software automation?*

To investigate this, we introduce **AI-Driven Self-Evolving Software** — a new form of software that **evolves continuously** through direct interaction with users.

We demonstrate this vision with a **lightweight prototype** built on a multi-agent architecture that:

* 🧩 Interprets user requirements autonomously
* 🖥️ Generates and validates code
* 🔄 Integrates new functionalities seamlessly

Case studies across multiple scenarios show that the prototype can **reliably construct and reuse functionality**, providing early evidence that such systems can scale to sophisticated applications — paving the way toward **truly automated software development**.

---

## 🎬 Demo

![demo](demo.gif)

---

## ⚡ Requirements

* **Python ≥ 3.12.11**
* Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 📂 Directory Layout

```
repo/
├── src/        # Source code for unit-test
├── src-v2.0/        # Source code for cross validation
├── config.json # Configuration file
├── requirements.txt
├── demo.gif    # Demo GIF
└── README.md
```

---

## 🚀 Quick Start

1. Edit the `api_key` and `base_url` in the `config.json` file
2. Run the agent system:

```bash
python -m src.core.agent
```

---

✅ **Tip:** Make sure your Python environment is correctly set up before running the agent.
