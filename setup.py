from setuptools import setup, find_packages

setup(name='citrination-client',
      version='1.1.1',
      url='http://github.com/CitrineInformatics/python-citrination-client',
      description='Python client for accessing the Citrination api',
      packages=find_packages(),
      install_requires=[
          'requests==2.10.0'
      ])
