from algopy import (
    ARC4Contract,
    UInt64,
    Bytes,
    Txn,
    BoxRef,
    op,
)
from algopy.arc4 import abimethod


class P2PTorrent(ARC4Contract):

    @abimethod()
    def store_file(
        self,
        file_hash: Bytes,
        chunks: UInt64,
        signature: Bytes,
    ) -> Bytes:

        metadata = (
            op.itob(chunks)
            + Bytes(b"|")
            + signature
            + Bytes(b"|")
            + Txn.sender.bytes
        )

        box = BoxRef(key=file_hash)
        box.put(metadata)

        return Bytes(b"STORED")

    @abimethod(readonly=True)
    def get_file(self, file_hash: Bytes) -> Bytes:
        box = BoxRef(key=file_hash)
        return box.get(default=Bytes(b""))
