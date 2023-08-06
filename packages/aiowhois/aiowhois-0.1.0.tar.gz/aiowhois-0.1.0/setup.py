# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiowhois']

package_data = \
{'': ['*'], 'aiowhois': ['data/*']}

install_requires = \
['aiodns>=1.1,<2.0', 'aiohttp>=3.4,<4.0', 'tldextract>=2.2,<3.0']

setup_kwargs = {
    'name': 'aiowhois',
    'version': '0.1.0',
    'description': 'Python Asyncio WHOIS Protocol Client',
    'long_description': '# aiowhois\n\n[![image](https://img.shields.io/pypi/v/aiowhois.svg)](https://pypi.python.org/pypi/aiowhois)\n[![image](https://img.shields.io/pypi/l/aiowhois.svg)](https://pypi.python.org/pypi/aiowhois)\n[![image](https://img.shields.io/codecov/c/github/brunoalano/aiowhois/master.svg)](https://codecov.io/gh/brunoalano/aiowhois/branch/master)\n[![aiowhois Build status](https://travis-ci.org/brunoalano/aiowhois.svg)](https://travis-ci.org/brunoalano/aiowhois)\n\nAsyncio-based WHOIS supporting **legacy** and **RDAP** protocols.\n\n```python\n>>> import aiowhois\n\n>>> resolv = aiowhois.Whois(timeout=10)\n>>> parsed_whois = await resolv.query(my_domain)\n```\n\n## Why aiowhois?\n\nTODO\n',
    'author': 'Bruno Alano Medina',
    'author_email': 'bruno@std.sh',
    'url': 'https://github.com/brunoalano/aiowhois',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
