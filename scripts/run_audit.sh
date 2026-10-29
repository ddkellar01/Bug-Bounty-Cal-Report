#!/usr/bin/env bash
set -e

echo "[*] Initializing BugBounty-Cal-Report automated script runner..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[+] Running test suite..."
pytest tests/

echo "[+] Executing default audit pipeline..."
python3 src/orchestrator.py --target "https://api.example.com/v1/users" --vector "AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:H/A:N"
