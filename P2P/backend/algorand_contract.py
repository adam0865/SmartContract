from algosdk.transaction import ApplicationNoOpTxn
from algosdk.atomic_transaction_composer import (
    AtomicTransactionComposer,
    TransactionWithSigner
)
from algorand_connector import algod_client, SENDER, signer, APP_ID

STORE_FILE_SELECTOR = bytes.fromhex("91e0a3d0")

def arc4_bytes(data: bytes) -> bytes:
    return len(data).to_bytes(2, "big") + data

def arc4_uint64(value: int) -> bytes:
    return value.to_bytes(8, "big")

def store_file_metadata(file_hash: str, chunks: int, signature: bytes):
    params = algod_client.suggested_params()
    params.flat_fee = True
    params.fee = 1000

    box_name = file_hash.encode()

    app_args = [
        STORE_FILE_SELECTOR,
        arc4_bytes(file_hash.encode()),
        arc4_uint64(chunks),
        arc4_bytes(signature),
    ]

    txn = ApplicationNoOpTxn(
        sender=SENDER,
        sp=params,
        index=APP_ID,
        app_args=app_args,
        boxes=[(APP_ID, box_name)]
    )

    atc = AtomicTransactionComposer()
    atc.add_transaction(TransactionWithSigner(txn, signer))
    result = atc.execute(algod_client, 4)

    print("✅ TX berhasil:", result.tx_ids)
    return result.tx_ids
