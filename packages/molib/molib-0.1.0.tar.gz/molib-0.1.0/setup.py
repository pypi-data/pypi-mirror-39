# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['molib']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0,<4.0']

setup_kwargs = {
    'name': 'molib',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Manny Ochoa',
    'author_email': 'manny@manuelochoa.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
