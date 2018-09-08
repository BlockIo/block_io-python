# BlockIo

This Python package is the official reference client for the Block.io payments API. To use this, you will need the Dogecoin, Bitcoin, or Litecoin API key(s) from <a href="https://block.io" target="_blank">Block.io</a>. Go ahead, sign up :)

#### ATTENTION: Package name has changed from block_io to block-io for PyPi.
#### COMPATIBILITY: Please use Python2.7+. Also compatible with Python 3.0+.

## Installation

[Using virtualenv is recommended when installing Python packages](https://packaging.python.org/en/latest/installing.html#virtual-environments).

Install the package using `pip` for **Python 2.7+**:

    pip install block-io

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

## Windows Users, Please Note:

You can install it like so on Windows: "pip install block-io==1.1.8"  

Now regarding the vcvarsall.bat error -- that error is due to the fact that pycrypto library is being compiled when you're trying to install the block-io library.  

The issue here is the missing MinGW32 compiler in Windows. You can install it [from here](http://sourceforge.net/projects/mingw/files/). Get the installer, install all the packages the install shows for MinGW32.  

After that, add the following to the PATH environment variable in your Control Panel -> System -> Advanced Settings:  

    C:\MinGW\bin\;C:\MinGW\mingw32\bin\;C:\MinGW\msys\1.0\bin\;C:\MinGW\msys\1.0\sbin\;  

Once this is done, go to C:\Python3.4\Lib\distutils, and create a file calls "distutils.cfg" with the following content:  

    [build]  

    compiler=mingw32  


Now exit your Command Prompt or Python IDE, go to Command Prompt again, type "pip install block-io==1.1.8". 


## Contributing

1. Fork it ( https://github.com/BlockIo/block_io-python/fork )
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request
