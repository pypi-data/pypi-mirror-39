# User Guide

## Introduction

Python SDK for Fairsense config center.

### Features

### Supported Python：

1. Python 2.6
2. Python 2.7
3. Python 3.3
4. Python 3.4
5. Python 3.5
6. Python 3.6

### Supported ACM version
1. ACM 1.0

### Change Logs

## Installation

For Python 2.7 and above:
```shell
pip install fc-config
```

For Python 2.6:
```shell
# install setuptools first:
wget https://pypi.io/packages/source/s/setuptools/setuptools-33.1.1.zip
unzip setuptools-33.1.1.zip
cd setuptools-33.1.1 && sudo python setup.py install

# if setuptools already exists:
sudo easy_install fc-config
```

## Getting Started


## Configuration
```
```

* *endpoint* - **required**  -  config center server address.
* *namespace* - Namespace. | default: `DEFAULT_TENANT`
* *ak* - AccessKey For Config Center. | default: `None`
* *sk* - SecretKey For Config Center. | default: `None`

#### Extra Options
Extra option can be set by `set_options`, as following:

```
client.set_options({key}={value})
```

Configurable options are:

## Use RAM

Example:
```python

```





