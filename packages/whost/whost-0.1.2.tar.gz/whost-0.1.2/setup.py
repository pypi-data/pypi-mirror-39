# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['whost', 'whost.ui']

package_data = \
{'': ['*']}

install_requires = \
['PyYaml>=3.13,<4.0',
 'colorama>=0.4.1,<0.5.0',
 'humanfriendly>=4.17,<5.0',
 'ipython>=7.2,<8.0',
 'netifaces>=0.10.7,<0.11.0',
 'requests>=2.21,<3.0',
 'tabulate>=0.8.2,<0.9.0',
 'unidecode>=1.0,<2.0']

setup_kwargs = {
    'name': 'whost',
    'version': '0.1.2',
    'description': 'Cardshop Writer Host Tools',
    'long_description': None,
    'author': 'renaud gaudin',
    'author_email': 'reg@kiwix.org',
    'url': 'https://www.kiwix.org/kiwix-hotspot/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
