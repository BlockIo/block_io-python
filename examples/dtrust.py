# This script demonstrates use of 4 of 5 MultiSig addresses with the Distributed Trust API
# at Block.io. Each key can be signed separately -- perfect for escrow, a variety of security
# architectures, and ofcourse, for personal use + cold storage of savings.
#
# Any questions? Contact support@block.io.

from block_io import BlockIo
from decimal import *
import json
import six # for python2 back-compatibility in printing messages using print as a function
import random
import sys
import os

version = 2 # API version

# use a testnet api key here, say, dogecoin
block_io = BlockIo(os.environ.get('BLOCK_IO_API_KEY'), os.environ.get('BLOCK_IO_PIN'), version)
getcontext().prec = 8 # coins are 8 decimal places at most

# create a new address with a random label
address_label = 'dtrust'+str(int(random.random()*10000))

# create the key objects for each private key
keys = [ BlockIo.Key.from_passphrase('alpha1alpha2alpha3alpha4'.encode('utf-8')), BlockIo.Key.from_passphrase('alpha2alpha3alpha4alpha1'.encode('utf-8')), BlockIo.Key.from_passphrase('alpha3alpha4alpha1alpha2'.encode('utf-8')), BlockIo.Key.from_passphrase('alpha4alpha1alpha2alpha3'.encode('utf-8')) ]

pubkeys = []

for key in keys:
    pubkeys.insert(len(pubkeys), key.pubkey_hex().decode("utf-8"))
    six.print_(key.pubkey_hex())

# create a dTrust address that requires 4 out of 5 keys (4 of ours, 1 at Block.io).
# Block.io automatically adds +1 to specified required signatures because of its own key

six.print_("* Creating a new 4 of 5 MultiSig address for DOGETEST")
six.print_(','.join(str(x) for x in pubkeys))
response = block_io.get_new_dtrust_address(label=address_label,public_keys=','.join(str(x) for x in pubkeys),required_signatures=3) 

# if you want this to be a green address (instant coin usage), add make_green=1 to the above call's parameters
# if choosing a green address, you will not receive a redeem_script in the response
# this is because Block.io must guarantee against double spends for green addresses

# what's our new address?
new_dtrust_address = response['data']['address']
six.print_(">> New dTrust Address on Network=", response['data']['network'], "is", new_dtrust_address)

# save this redeem script so you can use this address without depending on Block.io
six.print_(">> Redeem Script:", response['data']['redeem_script'])

# let's deposit some coins into this dTrust address of ours
six.print_("* Sending 50 DOGETEST to", new_dtrust_address)
response = block_io.withdraw_from_labels(from_labels='default', to_addresses=new_dtrust_address, amounts='50')
six.print_(">> Transaction ID:", response['data']['txid']) # you can check this on SoChain or any other blockchain explorer immediately

# since the above coins are coming from a Block.io green address (label=default, 2 of 2, visible on dashboard at Block.io),
# they are spendable instantly
# let's do that: spend coins from our dTrust address
six.print_("* Getting address balance for", new_dtrust_address)
response = block_io.get_dtrust_address_balance(address=new_dtrust_address)
available_balance = response['data']['available_balance']
six.print_(response)

six.print_(">> Available Balance in", new_dtrust_address, "is", available_balance, response['data']['network'])

# let's send coins back to the default address we withdraw from just now
# use high precision decimals when dealing with money (8 decimal places)
amount_to_send = Decimal(available_balance) - Decimal('1.0') # the amount minus the network fee needed to transact it

six.print_("* Sending", "%0.8f" % amount_to_send, "back to 'default' address")

# detour: what was our default address for the Dogecoin Testnet?
default_address = block_io.get_address_by_label(label='default')['data']['address']
six.print_(">> 'default' address:", default_address)

# create the withdrawal request
six.print_("* Creating withdrawal request")

response = block_io.withdraw_from_dtrust_addresses(from_addresses=new_dtrust_address,to_addresses=default_address,amounts=("%0.8f" % amount_to_send))

# the response contains data to sign and all the public_keys that need to sign it
# you can distribute this response to all of your machines the contain your private keys
# and have them inform block.io after signing the data
# from anywhere, you can then finalize the transaction

# below, we take this response, extract the data to sign, sign it and inform Block.io of the signatures right after we make them
# for one key at a time
six.print_(">> Withdrawal Reference ID:", response['data']['reference_id'])

# sign the withdrawal request, one signature at a time

for key in keys:

    pub_hex = key.pubkey_hex().decode("utf-8")
    
    for input in response['data']['inputs']:
        
        data_to_sign = input['data_to_sign']

        # find the object to put our signature in
        for signer in input['signers']:
            
            if signer['signer_public_key'] == pub_hex:
                # found it, let's add the signature to this object
                signer['signed_data'] = key.sign_hex(data_to_sign).decode("utf-8")

                six.print_("* Data Signed By:", pub_hex)

    # let's have Block.io record this signature we just created
    block_io.sign_transaction(signature_data=json.dumps(response['data']))
    six.print_(">> Signatures relayed to Block.io for Public Key=", pub_hex)

# finalize the transaction now that's it been signed by all our keys
six.print_("* Finalizing transaction")
response = block_io.finalize_transaction(reference_id=response['data']['reference_id'])
six.print_(">> Transaction ID:", response['data']['txid'])
six.print_(">> Network Fee Incurred:", response['data']['network_fee'], response['data']['network'])

# Relevant dTrust API calls (Numbers 1 thru 7: they work the same way as their non-dTrust counterparts on https://block.io/api).
# For a list of parameters and how to use these calls, please refer to their equivalent counterparts at https://block.io/api
# For any help whatsoever, please reach support@block.io
# 1. get_dtrust_address_balance
# 2. get_dtrust_address_by_label
# 3. get_my_dtrust_addresses
# 4. get_new_dtrust_address -- as demonstrated above
# 5. get_dtrust_transactions
# 6. withdraw_from_dtrust_labels -- returns an object with data to sign, and the public keys of the private keys that need to sign them. Does not accept a PIN -- it's of no use in dTrust withdrawals.
# 7. withdraw_from_dtrust_addresses -- same as (6)
# 8. sign_and_finalize_withdrawal (signature_data is a JSON string) -- you can use this call to finalize the transaction and sign it in one API call if needed
#    for the nitty gritty on this call, see https://block.io/api/simple/signing
#
# Distributed Trust-only calls:
# Number 9 and 10 do not need an API Key
# 9. get_remaining_signers* (parameter: reference_id) -- tells you the public keys that are yet to sign the transaction
# 10. sign_transaction* (signature_data is a JSON string) -- as demonstrated above
# 11. finalize_transaction* -- as demonstrated above
#   
#    API Calls marked with * are specific to the Distributed Trust framework.

# end :)
