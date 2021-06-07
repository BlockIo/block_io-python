from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='block-io',
      version='2.0.4',
      description='The easiest way to integrate Bitcoin, Dogecoin and Litecoin in your applications. Sign up at Block.io for your API key.',
      url='https://github.com/BlockIo/block_io-python',
      author='Atif Nazir',
      author_email='a@block.io',
      license='MIT',
      packages=['block_io'],
      python_requires='>=3.6, <4',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[
          'requests>=2.25.0',
          'pycryptodome>=3.9.9,<4.0',
          'base58==2.1.0',
          'bitcoin-utils-fork-minimal==0.4.11.3'
      ],
      zip_safe=False)
