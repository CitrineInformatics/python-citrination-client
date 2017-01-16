from setuptools import setup, find_packages

setup(name='citrination-client',
      version='1.2.0',
      url='http://github.com/CitrineInformatics/python-citrination-client',
      description='Python client for accessing the Citrination api',
      packages=find_packages(),
      install_requires=[
          'requests==2.10.0',
          'pypif==1.0.24',
          'six==1.10.0'
      ])
