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
    'version': '0.1.3',
    'description': 'Cardshop Writer Host Tools',
    'long_description': '# Cardshop Writer Host\n\n## Setup\n\n1. Install Ubuntu 18.04.1 LTS server with default options (see bellow)\n* log-in and elevate as `root` (`sudo su -`)\n* Make sure internet is working\n* download/copy your tunnel private key to `/root/.ssh/tunnel`\n* download setup script `curl -O /tmp/whost-setup https://raw.githubusercontent.com/kiwix/cardshop/master/whost/whost-setup`\n* run the setup script `chmod +x /tmp/whost-config && REVERSE_SSH_PORT=XXX /tmp/whost-config`\n\n### Ubuntu Install\n\nJust a regular, fresh Ubuntu-server install. Bellow are the defaults used for tests.\n\n1. Boot off the install media & select *Install Ubuntu Server* at grub prompt.\n* Select language (*English*)\n* Select Keyboard layout (*English (US)*, *English (US)*)\n* Select *Install Ubuntu* (not cloud instance)\n* Configure the network (*eth via dhcp*)\n* Proxy Address: none\n* Mirror Address: http://archive.ubuntu.com/ubuntu (pre-filled default)\n* *Use an entire Disk*\n* Choose disk to install to: *selected disk*\n* Summary: confirm and continue\n* Profile\n * name: `maint`\n * server name: whatever (`bkored`)\n * username: `maint`\n * password: `maint`\n * Import Identity: *from github* > `rgaudin`\n* *Reboot now*\n* Remove install media then `ENTER`\n \n \n',
    'author': 'renaud gaudin',
    'author_email': 'reg@kiwix.org',
    'url': 'https://www.kiwix.org/kiwix-hotspot/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
