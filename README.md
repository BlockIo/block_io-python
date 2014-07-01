# BlockIo

This Ruby Gem is the official reference client for the Block.io payments API. To use this, you will need the Dogecoin, Bitcoin, or Litecoin API key(s) from <a href="https://block.io" target="_blank">Block.io</a>. Go ahead, sign up :)

## Installation

Install the package using pip:

    $ sudo pip install block_io

Or install using easy_install:

    $ sudo easy_install block_io

## Usage

It's super easy to get started. In your Python shell, do:

    from block_io import BlockIo

    block_io = BlockIo('API KEY')

    # print the account balance
    print block_io.get_balance()
    
    # print all addresses on this account
    print block_io.get_my_addresses()

    # print the response of a withdrawal request
    print block_io.withdraw(pin='SECRET PIN', from_user_ids='1,2', to_user_id='0', amount='50.0')

For more information, see https://block.io/api. This Python client provides a mapping for all methods listed on the Block.io API site.

## Contributing

1. Fork it ( https://github.com/[my-github-username]/block_io/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request