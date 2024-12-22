from setuptools import setup, find_packages

VERSION = '0.1.1'

setup(
  name='trackmania-nations-forever-client',
  version=VERSION,
  description='An XML RPC client for Trackmania Nations Forever dedicated servers.',
  packages=find_packages(),
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url="https://github.com/Kaindorf-Games/trackmania-nations-forever-client",
)
