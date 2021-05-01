# Sweeps the entire balance (including unconfirmed transactions) from a given address
# You must provide the private key in Wallet Import Format for this to work
#                                                                                                                                    
# IMPORTANT!                                                                                                                         
# Must use Block.io API V2                                                                                            
# Must use API Key for the network your sweep addresses belong to                                                       
#                                                                                                                         
# Any issues? Contact support@block.io

from block_io import BlockIo
import json
import os

# must use private key of the address we're trying to sweep from
private_key = os.environ.get('PRIVATE_KEY') # this key never goes to Block.io, it stays here with you

to_address = os.environ.get('TO_ADDRESS') # the address to send coins to

api_version = 2 # must use API V2
block_io = BlockIo(os.environ.get('BLOCK_IO_API_KEY'), "", api_version)

try:

    prepared_transaction = block_io.prepare_sweep_transaction(private_key=private_key, to_address=to_address)

    # print the summary, but inspect the prepared transaction in-depth yourself
    print("Summary=", json.dumps(block_io.summarize_prepared_transaction(prepared_transaction)))

    created_transaction = block_io.create_and_sign_transaction(prepared_transaction)

    response = block_io.submit_transaction(transaction_data=created_transaction)

    print("Sweep Complete. Transaction ID:", response['data']['txid'])
    
except (Exception) as err:
    print(err)
    
