# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sqlite3_backup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sqlite3-backup',
    'version': '0.1.1',
    'description': 'implements missing backup functionality in sqlite3 module',
    'long_description': None,
    'author': 'Uwe Schmitt',
    'author_email': 'uwe.schmitt@id.ethz.ch',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
