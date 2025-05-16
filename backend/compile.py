from pyteal import *
from algosdk.v2client import algod
from algosdk.future.transaction import StateSchema
from algosdk import account, mnemonic
from algosdk.future.transaction import ApplicationCallTxn, OnComplete
from algosdk.atomic_transaction_composer import TransactionWithSigner, AtomicTransactionComposer
from algosdk.logic import get_application_address
import os

algod_address = "http://localhost:4001"
algod_token = "youralgodtoken"
algod_client = algod.AlgodClient(algod_token, algod_address)

from approval import approval
from clear import clear

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return bytes.fromhex(compile_response['result'])

approval_teal = compileTeal(approval(), mode=Mode.Application)
clear_teal = compileTeal(clear(), mode=Mode.Application)

with open("approval.teal", "w") as f:
    f.write(approval_teal)

with open("clear.teal", "w") as f:
    f.write(clear_teal)
