# About

This package is an implementation of the [Citrination API](http://citrineinformatics.github.io/api-documentation) written in python.

# Installation

To install the citrination_client package:

1. Clone this package to your machine
2. From the new directory run `python setup.py install`

# Using This Client

A more detailed discussion of the citrination API and usage are available at [http://citrineinformatics.github.io/api-documentation](http://citrineinformatics.github.io/api-documentation). Briefly, a new client to access the main citrination.com API can be generated using the following code:

```python
from citrination_client import CitrinationClient
client = CitrinationClient('your-api-token')
```

`your-api-token` is a [unique API token](http://citrineinformatics.github.io/api-documentation/?python#api-token) that is associated with your citrination.com account.

To access a sub-domain (e.g. your-site.citrination.com), use:

```python
from citrination_client import CitrinationClient
client = CitrinationClient('your-api-token', 'https://your-site.citrination.com')
```
