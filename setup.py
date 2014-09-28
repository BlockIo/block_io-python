from setuptools import setup

setup(name='block_io',
      version='0.1.3',
      description='The easiest way to create a Dogecoin, Bitcoin, or Litecoin wallet. Sign up at Block.io for your API key.',
      url='http://github.com/blockio/blockio-python',
      author='Atif Nazir',
      author_email='a@block.io',
      license='MIT',
      packages=['block_io'],
      install_requires=[
          'requests',
          'pycrypto',
          'hashlib'
      ],
      zip_safe=False)

# for packages not on pypi
# dependency_links=['http://github.com/user/repo/tarball/master#egg=package-1.0']
