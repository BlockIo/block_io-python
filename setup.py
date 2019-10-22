from setuptools import setup

setup(name='block-io',
      version='1.1.10',
      description='The easiest way to integrate Bitcoin, Dogecoin and Litecoin in your applications. Sign up at Block.io for your API key.',
      url='https://github.com/BlockIo/block_io-python',
      author='Atif Nazir',
      author_email='a@block.io',
      license='MIT',
      packages=['block_io'],
      install_requires=[
          'requests>=2.20.0',
          'pycryptodome>=3.6.6,<4.0',
          'ecdsa==0.13.3',
          'six>=1.8.0',
          'base58>=1.0.0'
      ],
      zip_safe=False)

# for packages not on pypi
# dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0']
