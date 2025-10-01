# AI-Driven Self-Evolving Software

## Introduction
This repository contains the implementation and experimental code for the paper:

**AI-Driven Self-Evolving Software**

This repository aims to provide:
- A working implementation of the core algorithm presented in the paper.
- Scripts and configuration files to reproduce the reported experiments.

## Abstract
Software automation has long been a central goal of software engineering, aiming to minimize human intervention in the development lifecycle. 
Recent efforts have leveraged Artificial Intelligence (AI) to advance software automation with notable progress. However, current AI functions primarily as assistants to human developers, leaving software development still dependent on explicit human intervention.

This raises a fundamental question: \textit{Can AI move beyond its role as an assistant to become a core component of software, thereby enabling genuine software automation?} 

To investigate this vision, we introduce \textbf{AI-Driven Self-Evolving Software}, a new form of software that evolves continuously through direct interaction with users. 

We demonstrate the feasibility of this idea with a lightweight prototype built on a multi-agent architecture that autonomously interprets user requirements, generates and validates code, and integrates new functionalities. Case studies across multiple representative scenarios show that the prototype can reliably construct and reuse functionality, providing early evidence that such software systems can scale to more sophisticated applications and pave the way toward truly automated software development.

## demo

![demo](demo.gif)

## Requirements
- Python 3.12.11 or newer
- Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Directory layout
```
repo/
├── src/        # Source code
├── config.json # Configuration file
├── requirements.txt
├── demo.gif
└── README.md
```

## Quick start

* Edit the ```api_key``` and ```base_url``` in the ```config.json``` file

* run the following command to interact with agent systems:
```bash
python -m src.core.agent
```
