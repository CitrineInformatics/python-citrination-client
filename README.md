# Python Citrination Client
[![Build Status](https://travis-ci.org/CitrineInformatics/python-citrination-client.svg?branch=master)](https://travis-ci.org/CitrineInformatics/python-citrination-client)

## About

This package is an implementation of the Citrination API.

## Installation

### Requirements
 * Python >= 2.7.10 or >= 3.4
 
### Setup

```shell
$ pip install citrination-client
```

There are known issues installing libraries that depend on six on OSX. If you
have issues installing this library, run the following command:

```
$ pip install --ignore-installed six citrination-client
```

### Legacy information

In order to interact with older versions of Citrination, please clone
the legacy branch on this repo.


### Troubleshooting

It is possible that you will run into problems if you are using an older
version of OpenSSL and running MacOSX. If the following error happens when
using the requests library to retrieve information from citrination:

```
requests.exceptions.SSLError: ("bad handshake: Error([('SSL routines', 'SSL23_GET_SERVER_HELLO', 'sslv3 alert handshake failure')],)",)
```

Check to see that you are using a current version of OpenSSL. This error was
first encountered using `OpenSSL 0.9.8zh 14 Jan 2016`, and was resolved by
upgrading to `OpenSSL 1.0.2j 26 Sep 2016`.

After upgrading OpenSSL, make sure that your python installation is using the
correct version:

```
python -c "import ssl; print ssl.OPENSSL_VERSION"
```

Some useful guides can be found [here](http://stackoverflow.com/questions/24323858/python-referencing-old-ssl-version) and [here](https://comeroutewithme.com/2016/03/13/python-osx-openssl-issue/). 
