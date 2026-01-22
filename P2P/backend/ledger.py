import json
import os
import time

LEDGER_FILE = "ledger.json"

if not os.path.exists(LEDGER_FILE):
    with open(LEDGER_FILE, "w") as f:
        json.dump({"files": []}, f)

def add_file(file_hash, chunks, signature):
    with open(LEDGER_FILE) as f:
        ledger = json.load(f)

    ledger["files"].append({
        "hash": file_hash,
        "chunks": len(chunks),
        "timestamp": time.time(),
        "signature": signature.hex()
    })

    with open(LEDGER_FILE, "w") as f:
        json.dump(ledger, f, indent=2)

def get_summary():
    with open(LEDGER_FILE) as f:
        ledger = json.load(f)

    return {
        "files_registered": len(ledger["files"]),
        "files_keys_sample": [f["hash"] for f in ledger["files"][:5]]
    }
