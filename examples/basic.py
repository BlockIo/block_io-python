# Basic example for using Block.io for generating wallet addresses and withdrawing coins

from block_io import BlockIo
from decimal import *
import os
import random
import sys
import json

version = 2 # API version

# use a testnet api key here, say, dogecoin
block_io = BlockIo(os.environ.get('BLOCK_IO_API_KEY'), os.environ.get('BLOCK_IO_PIN'), version)

# create a new address with a random label
address_label = 'tlabel'+str(int(random.random()*10000))

new_address = None

try:
    new_address = block_io.get_new_address(label=address_label)['data']['address']
except Exception:
    exc = sys.exc_info()[1]
    print(exc)

if (new_address is None):
    # the address label already existed, let's get the associated address
    new_address = block_io.get_address_by_label(label=address_label)['data']['address']

print("Address Generated for Label=",address_label,":",new_address)

# get address balance
available_balance = Decimal('0.0')
try:
    response = block_io.get_address_balance(label=address_label)
    available_balance = Decimal(response['data']['available_balance'])
    network = response['data']['network']
    print("Available Balance in Label=",address_label,":",format(available_balance,'.8f'),network)
except Exception:
    exc = sys.exc_info()[1]
    print(exc)

# get total balance on the account
try:
    response = block_io.get_balance()
    available_balance = Decimal(response['data']['available_balance'])
    network = response['data']['network']
    print("Total Balance in Account=",format(available_balance,'.8f'),network)
except Exception:
    exc = sys.exc_info()[1]
    print(exc)

# send 1% of the coins in our account to our new label's address
try:
    amount_to_send = Decimal(0.01) * available_balance
    print("Sending Coins=",format(amount_to_send,'.8f'),"to Label=",address_label)

    # prepare the transaction
    prepared_transaction = block_io.prepare_transaction(to_label=address_label, amount=format(amount_to_send, '.8f'))

    # review its response
    # for in-depth information about the transaction you will create, look at the prepared_transaction object directly
    print(json.dumps(block_io.summarize_prepared_transaction(prepared_transaction)))

    # once satisfied, create the transaction and sign it
    created_transaction_and_signatures = block_io.create_and_sign_transaction(prepared_transaction)

    # inspect the transaction_data (particularly the tx_hex) to ensure it is what you wanted
    # once satisfied, submit the transaction to Block.io for its signature + broadcast to the peer-to-peer network
    response = block_io.submit_transaction(transaction_data=created_transaction_and_signatures)
    
    print("Coins sent. Transaction ID=", response['data']['txid'])
except Exception:
    exc = sys.exc_info()[1]
    print(exc)

# get the new balance on our new address
try:
    response = block_io.get_address_balance(label=address_label)
    available_balance = Decimal(response['data']['available_balance'])
    network = response['data']['network']
    
    print("New Balance in Label=",address_label+":",format(available_balance,'.8f'),network)
except Exception:
    exc = sys.exc_info()[1]
    print(exc)

# end :)
