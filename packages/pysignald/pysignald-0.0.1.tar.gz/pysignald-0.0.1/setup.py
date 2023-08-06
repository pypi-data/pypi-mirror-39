# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['signald']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=18.2,<19.0']

setup_kwargs = {
    'name': 'pysignald',
    'version': '0.0.1',
    'description': 'A library that allows communication via the Signal IM service using the signald daemon.',
    'long_description': None,
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
