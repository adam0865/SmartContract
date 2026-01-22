from algosdk.v2client import algod
from algosdk import mnemonic, account
from algosdk.atomic_transaction_composer import AccountTransactionSigner

# =====================================================
# ALGOD CLIENT (LOCALNET / ALGOKIT)
# =====================================================
ALGOD_ADDRESS = "http://localhost:4001"
ALGOD_TOKEN = "a" * 64  # default AlgoKit / sandbox

algod_client = algod.AlgodClient(
    ALGOD_TOKEN,
    ALGOD_ADDRESS
)

# =====================================================
# ACCOUNT (MNEMONIC HASIL goal account export)
# =====================================================
MNEMONIC = (
    "feel list agree open scissors whale have bunker slush often mosquito alpha surprise ensure glow utility barely dilemma person burger usual dilemma unknown able agree"
)

PRIVATE_KEY = mnemonic.to_private_key(MNEMONIC)
SENDER = account.address_from_private_key(PRIVATE_KEY)

signer = AccountTransactionSigner(PRIVATE_KEY)

# =====================================================
# SMART CONTRACT APP ID
# =====================================================
APP_ID = 1002  # SESUAI HASIL DEPLOY
