# BlockIo

This Python package is the official reference client for the Block.io payments API. To use this, you will need the Dogecoin, Bitcoin, or Litecoin API key(s) from <a href="https://block.io" target="_blank">Block.io</a>. Go ahead, sign up :)

# ATTENTION: Package name has changed from block_io to block-io for PyPi.
# COMPATIBILITY: Please use Python2.6+. Also compatible with Python 3.0+.

## Installation

[Using virtualenv is recommended when installing Python packages](https://packaging.python.org/en/latest/installing.html#virtual-environments).

Install the package using `pip` for **Python 3**:

    pip install block-io

Install the package using `pip` for **Python 2** - backported hashlib is required:

    pip install block-io hashlib==20081119

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
