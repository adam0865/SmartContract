from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os, shutil, json

# === Local Modules ===
from torrent import split_file, rebuild_file, hash_file
from crypto import sign
from ledger import add_file, get_summary
from nodes import register_node, get_nodes
from algorand_contract import store_file_metadata

app = FastAPI()

STORAGE = "storage"
os.makedirs(STORAGE, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# UPLOAD
# ======================================================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    original_name = file.filename
    content_type = file.content_type or "application/octet-stream"

    file_path = os.path.join(STORAGE, original_name)
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    file_hash = hash_file(file_path)
    chunk_dir = os.path.join(STORAGE, file_hash)
    chunks = split_file(file_path, chunk_dir)

    # === SAVE METADATA (INI YANG SEBELUMNYA HILANG)
    meta = {
        "filename": original_name,
        "content_type": content_type
    }

    with open(os.path.join(chunk_dir, "meta.json"), "w") as f:
        json.dump(meta, f)

    signature = sign(file_hash.encode())
    add_file(file_hash, chunks, signature)

    tx_ids = store_file_metadata(
        file_hash=file_hash,
        chunks=len(chunks),
        signature=signature
    )

    return {
        "status": "stored",
        "file_hash": file_hash,
        "filename": original_name,
        "chunks": len(chunks),
        "algorand_tx": tx_ids
    }

# ======================================================
# ALIAS FOR FRONTEND
# ======================================================
@app.post("/upload_with_file")
async def upload_with_file(file: UploadFile = File(...)):
    return await upload_file(file)

# ======================================================
# VERIFY
# ======================================================
@app.get("/verify/{file_hash}")
def verify(file_hash: str):
    return {
        "exists": os.path.exists(os.path.join(STORAGE, file_hash))
    }

# ======================================================
# DOWNLOAD (REAL FILE)
# ======================================================
@app.get("/download/{file_hash}")
def download(file_hash: str):
    chunk_dir = os.path.join(STORAGE, file_hash)
    if not os.path.exists(chunk_dir):
        return {"detail": "File not found"}

    meta_path = os.path.join(chunk_dir, "meta.json")
    if not os.path.exists(meta_path):
        return {"detail": "Metadata missing"}

    with open(meta_path) as f:
        meta = json.load(f)

    filename = meta["filename"]
    content_type = meta["content_type"]

    chunks = sorted(
        os.path.join(chunk_dir, c)
        for c in os.listdir(chunk_dir)
        if c.startswith("chunk_")
    )

    output_path = os.path.join(STORAGE, filename)
    rebuild_file(chunks, output_path)

    return FileResponse(
        path=output_path,
        filename=filename,
        media_type=content_type
    )

# ======================================================
# NODE
# ======================================================
@app.post("/register_node")
def register(address: str = Form(...)):
    return register_node(address)

@app.get("/nodes")
def nodes():
    return get_nodes()

# ======================================================
# LEDGER
# ======================================================
@app.get("/summary")
def summary():
    return get_summary()
