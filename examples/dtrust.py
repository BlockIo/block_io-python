# This script demonstrates use of 4 of 5 MultiSig addresses with the Distributed Trust API
# at Block.io. Each key can be signed separately -- perfect for escrow, a variety of security
# architectures, and ofcourse, for personal use + cold storage of savings.
#
# Any questions? Contact support@block.io.

from block_io import BlockIo
from decimal import Decimal
import json
import random
import sys
import os

version = 2 # API version

# use a testnet api key here, say, dogecoin
block_io = BlockIo(os.environ.get('BLOCK_IO_API_KEY'), os.environ.get('BLOCK_IO_PIN'), version)

# create a new address with a random label
address_label = 'dtrust'+str(int(random.random()*10000))

# create the key objects for each private key
# WARNING: generate your own keys, these are just for demonstrating
# key = BlockIo.Key.generate()
# key.pubkey_hex().decode('utf-8') # store this yourself
# key.privkey_hex().decode('utf-8') # store this yourself
keys = [
            "b515fd806a662e061b488e78e5d0c2ff46df80083a79818e166300666385c0a2",
            "1584b821c62ecdc554e185222591720d6fe651ed1b820d83f92cdc45c5e21f",
            "2f9090b8aa4ddb32c3b0b8371db1b50e19084c720c30db1d6bb9fcd3a0f78e61",
            "6c1cefdfd9187b36b36c3698c1362642083dcc1941dc76d751481d3aa29ca65"
        ]

pubkeys = []

# get the compressed public keys for our private keys
for key in keys:
    pubkeys.insert(len(pubkeys), BlockIo.Key.from_privkey_hex(key).pubkey_hex().decode("utf-8"))
    print(pubkeys[-1]) # key.pubkey_hex())

# create a dTrust address that requires 4 out of 5 keys (4 of ours, 1 at Block.io).
# Block.io automatically adds +1 to specified required signatures because of its own key

print("* Creating a new 4 of 5 MultiSig address for DOGETEST")
print(','.join(str(x) for x in pubkeys))
response = block_io.get_new_dtrust_address(label=address_label,public_keys=','.join(str(x) for x in pubkeys),required_signatures=3) 

# if you want this to be a green address (instant coin usage), add make_green=1 to the above call's parameters
# if choosing a green address, you will not receive a redeem_script in the response
# this is because Block.io must guarantee against double spends for green addresses

# what's our new address?
new_dtrust_address = response['data']['address']
print(">> New dTrust Address on Network=", response['data']['network'], "is", new_dtrust_address)

# save this redeem script so you can use this address without depending on Block.io
print(">> Redeem Script:", response['data']['redeem_script'])

# let's deposit some coins into this dTrust address of ours
print("* Sending 50.12345678 DOGETEST to", new_dtrust_address)

# prepare the transaction
prepared_transaction = block_io.prepare_transaction(from_labels='default', to_addresses=new_dtrust_address, amounts='50.12345678')

# inspect it in-depth yourself, below is just a summary of the amounts being transacted
print("prepared transaction summary=", json.dumps(block_io.summarize_prepared_transaction(prepared_transaction)))

# create the transaction and its signatures
created_transaction_and_signatures = block_io.create_and_sign_transaction(prepared_transaction)

# once satisfied with the data in created_transaction_and_signatures, submit it to Block.io for its signature and to broadcast to the peer-to-peer network
response = block_io.submit_transaction(transaction_data=created_transaction_and_signatures)
      
print(">> Transaction ID:", response['data']['txid']) # you can check this on SoChain or any other blockchain explorer immediately

# since the above coins are coming from a Block.io green address (label=default, 2 of 2, visible on dashboard at Block.io),
# they are spendable instantly
# let's do that: spend coins from our dTrust address
print("* Getting address balance for", new_dtrust_address)
response = block_io.get_dtrust_address_balance(address=new_dtrust_address)
available_balance = response['data']['available_balance']
print(response)

print(">> Available Balance in", new_dtrust_address, "is", available_balance, response['data']['network'])

# let's send coins back to the default address we withdraw from just now
# use high precision decimals when dealing with money (8 decimal places)
amount_to_send = Decimal(available_balance) - Decimal('1.0') # the amount minus the network fee needed to transact it

print("* Sending", "%0.8f" % amount_to_send, "back to 'default' address")

# detour: what was our default address for the Dogecoin Testnet?
default_address = block_io.get_address_by_label(label='default')['data']['address']
print(">> 'default' address:", default_address)

# create the withdrawal request
print("* Creating withdrawal request")

# see above for what these steps mean and what you should be doing
# this is just a quick demo
prepared_transaction = block_io.prepare_dtrust_transaction(from_addresses=new_dtrust_address, to_addresses=default_address, amounts=("%0.8f" % amount_to_send))

print(">> Network Fee To Incur:", block_io.summarize_prepared_transaction(prepared_transaction)['network_fee'])

# this signs the complete transaction here if you provide keys to get enough signatures to finalize the transaction
# otherwise the returned object contains the payload of the unsigned transaction you created locally, and the signatures you want to append to it
created_and_signed_transaction = block_io.create_and_sign_transaction(prepared_transaction, keys)

# submit it to Block.io to append its signatures if necessary, and broadcast the transaction to the peer-to-peer network
response = block_io.submit_transaction(transaction_data=created_and_signed_transaction)

print(">> Transaction ID:", response['data']['txid'])

# Relevant dTrust API calls
# For a list of parameters and how to use these calls, please refer to their equivalent counterparts at https://block.io/api
# For any help whatsoever, please reach support@block.io
# 1. get_dtrust_address_balance
# 2. get_dtrust_address_by_label
# 3. get_my_dtrust_addresses
# 4. get_new_dtrust_address -- as demonstrated above
# 5. get_dtrust_transactions
# 6. prepare_dtrust_transaction
#    API Calls marked with * are specific to the Distributed Trust framework.

# end :)
