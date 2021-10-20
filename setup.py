import PyWCGIshell as package
from setuptools import setup

setup(
    name=package.__name__,
    version=package.__version__,
    py_modules=[package.__name__],
    install_requires = [],
    author=package.__author__,
    author_email=package.__author_email__,
    maintainer=package.__maintainer__,
    maintainer_email=package.__maintainer_email__,
    description=package.__description__,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=package.__url__,
    project_urls = {
        "Documentation": "https://mauricelambert.github.io/info/python/security/PyWCGIshell.html"
    },
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
        "Topic :: Security",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
    ],
    python_requires='>=3.6',
    keywords=[
        "WebShell",
        "Server",
        "Web",
        "Hacking",
        "WSGI",
        "CGI",
        "Security",
    ],
    platforms=["Windows", "Linux", "MacOS"],
    license=package.__license__,
)