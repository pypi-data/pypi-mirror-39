# Uploading package to PyPi.

from setuptools import setup

setup(name='schoolopy',
      version='0.2.1',
      description='A Python wrapper for Schoology\'s API.',
      url='https://github.com/ErikBoesen/schoolopy',
      author='Erik Boesen',
      author_email='me@erikboesen.com',
      license='MIT',
      packages=['schoolopy'],
      install_requires=['requests', 'requests-oauthlib', 'oauthlib'],
      zip_safe=False)
