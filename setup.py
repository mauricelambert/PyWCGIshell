from setuptools import setup, find_packages
import PyWCGIshell

name = "Maurice Lambert"
email = "mauricelambert434@gmail.com"

setup(
    name = PyWCGIshell.__name__,
 
    version = PyWCGIshell.__version__,
    py_modules=[PyWCGIshell.__name__],
    install_requires = [],

    author=name,
    author_email=email,
    maintainer=name,
    maintainer_email=email,
 
    description = "This package implement a WebShell for CGI and WSGI server.",
    long_description = open('README.md').read(),
    long_description_content_type="text/markdown",
 
    include_package_data = True,

    url = 'https://github.com/mauricelambert/PyWCGIshell',
    project_urls = {
        "Documentation": "https://mauricelambert.github.io/info/python/security/PyWCGIshell.html"
    },
 
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Topic :: Security",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
 
    python_requires='>=3.6',
)