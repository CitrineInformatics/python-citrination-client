from setuptools import setup, find_packages

setup(name='citrination-client',
      version='1.5.0',
      url='http://github.com/CitrineInformatics/python-citrination-client',
      description='Python client for accessing the Citrination api',
      packages=find_packages(exclude=('docs')),
      install_requires=[
          'requests<3',
          'pypif',
          'six<2'
      ])
