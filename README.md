# BlockIo

This Python package is the official reference client for the Block.io payments API. To use this, you will need the Dogecoin, Bitcoin, or Litecoin API key(s) from <a href="https://block.io" target="_blank">Block.io</a>. Go ahead, sign up :)

### Latest version: 1.0.5. Now enforcing use of TLSv1 (instead of default SSLv3, which is vulnerable).

## Installation

Install the package using pip:

    $ sudo pip install block-io

Or install using easy_install:

    $ sudo easy_install block-io

## Usage

It's super easy to get started. In your Python shell, do:

    from block_io import BlockIo

    block_io = BlockIo('API KEY', 'SECRET PIN', API_VERSION)

    # print the account balance
    print block_io.get_balance()
    
    # print all addresses on this account
    print block_io.get_my_addresses()

    # print the response of a withdrawal request
    print block_io.withdraw(from_labels='default', to_label='destLabel', amount='50.0')

For more information, see [Python API Docs](https://block.io/api/simple/python). This Python client provides a mapping for all methods listed on the Block.io API site.

## Contributing

1. Fork it ( https://github.com/BlockIo/block_io-python/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
