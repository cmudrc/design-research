# IDETC 2026 AI Experiments Tutorial Setup

From this folder, run the block for your operating system.

## macOS or Linux

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python preflight.py
```

## Windows PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\python -m pip install --upgrade pip
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python preflight.py
```

Success ends with:

```text
Preflight passed. You are ready for the tutorial.
```
