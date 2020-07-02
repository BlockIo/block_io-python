from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setup(name='block-io',
      version='1.1.14',
      description='The easiest way to integrate Bitcoin, Dogecoin and Litecoin in your applications. Sign up at Block.io for your API key.',
      url='https://github.com/BlockIo/block_io-python',
      author='Atif Nazir',
      author_email='a@block.io',
      license='MIT',
      packages=['block_io'],
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[
          'requests>=2.20.0',
          'pycryptodome>=3.9.8,<4.0',
          'ecdsa==0.15',
          'six>=1.8.0',
          'base58==1.0.3'
      ],
      zip_safe=False)

