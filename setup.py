from setuptools import setup

setup(name='block-io',
      version='1.0.6',
      description='The easiest way to create a Dogecoin, Bitcoin, or Litecoin wallet. Sign up at Block.io for your API key.',
      url='https://github.com/BlockIo/block_io-python',
      author='Atif Nazir',
      author_email='a@block.io',
      license='MIT',
      packages=['block_io'],
      install_requires=[
          'requests',
          'pycrypto',
          'hashlib',
      ],
      zip_safe=False)

# for packages not on pypi
# dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0']
