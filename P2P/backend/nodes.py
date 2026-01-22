import time

nodes = {}

TIMEOUT = 30  # seconds

def register_node(address: str):
    nodes[address] = {
        "status": "online",
        "last_seen": time.time()
    }
    return nodes[address]

def heartbeat(address: str):
    if address in nodes:
        nodes[address]["last_seen"] = time.time()
        nodes[address]["status"] = "online"

def get_nodes():
    now = time.time()
    for addr, info in nodes.items():
        if now - info["last_seen"] > TIMEOUT:
            info["status"] = "offline"
    return nodes
