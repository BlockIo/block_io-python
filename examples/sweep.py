# Sweeps the entire balance (including unconfirmed transactions) from a given address
# You must provide the private key in Wallet Import Format for this to work
#                                                                                                                                    
# IMPORTANT!                                                                                                                         
# Must use Block.io API V2                                                                                            
# Must use API Key for the network your sweep addresses belong to                                                       
#                                                                                                                         
# Any issues? Contact support@block.io

from block_io import BlockIo
import six

# must use private key of the address we're trying to sweep from
private_key = 'PRIVATE KEY IN HEX FORM' # this key never goes to Block.io, it stays here with you

from_address = 'SWEEP COINS FROM THIS ADDRESS' # the address to sweep from
to_address = 'SWEEP COINS INTO THIS ADDRESS' # the address to send coins to

api_version = 2 # must use API V2
block_io = BlockIo('YOUR API KEY', 'PIN - NOT NEEDED HERE', api_version)

try:
    response = block_io.sweep_from_address(from_address=from_address,private_key=private_key,to_address=to_address)
    six.print_("Sweep Complete. Transaction ID:", response['data']['txid'])
except Exception, err:
    six.print_(err)

