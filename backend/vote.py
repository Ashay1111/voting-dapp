from algosdk import mnemonic, account
from algosdk.v2client import algod
from algosdk.future.transaction import ApplicationNoOpTxn
import time

algod_address = "http://localhost:4001"
algod_token = "youralgodtoken"
algod_client = algod.AlgodClient(algod_token, algod_address)

user_mnemonic = "user 25-word mnemonic here"
user_private_key = mnemonic.to_private_key(user_mnemonic)
user_address = account.address_from_private_key(user_private_key)

app_id = 123456
params = algod_client.suggested_params()

txn = ApplicationNoOpTxn(
    sender=user_address,
    sp=params,
    index=app_id,
    app_args=["voteA"]
)

signed_txn = txn.sign(user_private_key)
txid = algod_client.send_transaction(signed_txn)

response = algod_client.pending_transaction_info(txid)
while not response.get("confirmed-round"):
    time.sleep(1)
    response = algod_client.pending_transaction_info(txid)

print("Vote submitted in round", response["confirmed-round"])
