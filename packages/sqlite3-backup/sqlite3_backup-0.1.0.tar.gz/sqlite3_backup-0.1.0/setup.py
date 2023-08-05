# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sqlite3_backup']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'sqlite3-backup',
    'version': '0.1.0',
    'description': 'sqlite3 from the standard library does not support the backup\nfunctionality provided by the original sqlite3 c implementation.\n\nThis package fixes this by providing a simple backup function.\n\nTypical use case is to write an in-memory sqlite3-db to disk.\n\nThis package relies of ctypes module and thus does not require a\nworking c compiler setup.\n',
    'long_description': None,
    'author': 'Uwe Schmitt',
    'author_email': 'uwe.schmitt@id.ethz.ch',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
