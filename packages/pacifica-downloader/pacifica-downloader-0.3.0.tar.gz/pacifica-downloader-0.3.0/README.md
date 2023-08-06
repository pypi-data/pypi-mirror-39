# Pacifica Python Downloader
[![Build Status](https://travis-ci.org/pacifica/pacifica-python-downloader.svg?branch=master)](https://travis-ci.org/pacifica/pacifica-python-downloader)
[![Build Status](https://ci.appveyor.com/api/projects/status/38dmnpbm398cvtu9?svg=true)](https://ci.appveyor.com/project/dmlb2000/pacifica-python-downloader)
[![Test Coverage](https://api.codeclimate.com/v1/badges/e0d5aaf99dd05f3485d6/test_coverage)](https://codeclimate.com/github/pacifica/pacifica-python-downloader/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/e0d5aaf99dd05f3485d6/maintainability)](https://codeclimate.com/github/pacifica/pacifica-python-downloader/maintainability)

Pacifica Python Library for Downloading Data

This repository provides a library so python applications can
download data from Pacifica.

## Downloader API

The entrypoint for this library is the `Downloader` class in
the `downloader` module. Instances of this class are created
with a download directory and a
[Pacifica Cartd](https://github.com/pacifica/pacifica-cartd)
endpoint url.

### Downloader Class

The [constructor](pacifica/downloader/downloader.py#16) takes
two arguments `location` and `cart_api_url`. The `location` is
a download directory to be created by a download method. The
`cart_api_url` is the endpoint for creating carts.

The other methods in the `Downloader` class are the supported
download methods. Each method takes appropriate input for that
method and the method will download the data to the location
defined in the constructor.

[CloudEvents](https://github.com/cloudevents/spec) is a
standard for how to send messages between services in cloud
environments. The `cloudevent()` method
([here](pacifica/downloader/downloader.py#45))
consumes the event emitted by the
[Pacifica Notifications](https://github.com/pacifica/pacifica-notifications)
service and downloads the data.

## Internal Classes and Methods

The internal classes help organize the work around the cart API.

### Cart API

The [CartAPI](pacifica/downloader/cartapi.py#11) class has two
methods used for setting up a cart and waiting for completion.

The `setup_cart()` method takes a callable argument that returns
an iterator. The iterator returns a list that is directly sent to
the [Cartd API](https://github.com/pacifica/pacifica-cartd). The
`setup_cart()` method returns the full url to the cart created.

The `wait_for_cart()` method takes a cart url returned from the
`setup_cart()` method and polls the endpoint until the cart is
ready to download.

### CloudEvent

The `CloudEvent` class ([here](pacifica/downloader/cloudevent.py#7))
contains the `cloudevent()` method. It
requires the cloud event as an argument. The `cloudevent()`
generates a method that yields the cart file objects from the
cloud event.

## Examples

### CloudEvents Example

This is a basic stub code to download data from a cloud event.
This assumes the cloudevent is saved to a file for processing.
There are a number of ways to get the cloud event this is just
a minimum representation of whats required.

```
from json import loads
from tempfile import mkdtemp
from pacifica.downloader import Downloader

cloud_event = loads(open('cloudevent.json').read())
down_path = mkdtemp()
down = Downloader(down_path, 'http://metadata.example.com')
down.cloudevent(cloud_event)
```
