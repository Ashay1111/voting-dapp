from algosdk import account, mnemonic
from algosdk.v2client import algod
from algosdk.future.transaction import StateSchema, ApplicationCreateTxn
from base64 import b64decode
import json
import time

algod_address = "http://localhost:4001"
algod_token = "youralgodtoken"
algod_client = algod.AlgodClient(algod_token, algod_address)

creator_mnemonic = "your 25-word mnemonic here"
creator_private_key = mnemonic.to_private_key(creator_mnemonic)
creator_address = account.address_from_private_key(creator_private_key)

with open("approval.teal", "r") as f:
    approval_program = f.read()

with open("clear.teal", "r") as f:
    clear_program = f.read()

approval_result = algod_client.compile(approval_program)
clear_result = algod_client.compile(clear_program)

approval_bytes = b64decode(approval_result['result'])
clear_bytes = b64decode(clear_result['result'])

global_schema = StateSchema(num_uints=2, num_byte_slices=0)
local_schema = StateSchema(num_uints=1, num_byte_slices=0)

params = algod_client.suggested_params()

txn = ApplicationCreateTxn(
    sender=creator_address,
    sp=params,
    on_complete=0,
    approval_program=approval_bytes,
    clear_program=clear_bytes,
    global_schema=global_schema,
    local_schema=local_schema
)

signed_txn = txn.sign(creator_private_key)
txid = algod_client.send_transaction(signed_txn)

response = algod_client.pending_transaction_info(txid)
while not response.get("confirmed-round"):
    time.sleep(1)
    response = algod_client.pending_transaction_info(txid)

print("App ID:", response["application-index"])
