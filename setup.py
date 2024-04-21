from setuptools import setup, find_packages

setup(
  name='rconnet',
  version='0.0.3',
  author='VordyV',
  author_email='vordy.production@gmail.com',
  description='Python RCON client for the Battlefield 2142 server',
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  url='https://github.com/VordyV/rconnet',
  packages=find_packages(),
  keywords='rcon client',
  python_requires='>=3.11'
)