# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['importers']

package_data = \
{'': ['*']}

install_requires = \
['beancount>=2.1,<3.0', 'simplejson>=3.16,<4.0']

setup_kwargs = {
    'name': 'nobbofin-tools',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Enno Lohmeier',
    'author_email': 'enno@nerdworks.de',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
