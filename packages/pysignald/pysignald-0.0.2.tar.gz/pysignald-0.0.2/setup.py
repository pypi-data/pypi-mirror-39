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
    'version': '0.0.2',
    'description': 'A library that allows communication via the Signal IM service using the signald daemon.',
    'long_description': 'pysignald\n=======\n\n[![pipeline status](https://gitlab.com/stavros/pysignald/badges/master/pipeline.svg)](https://gitlab.com/stavros/pysignald/commits/master)\n\npysignald is a Python client for the excellent [signald](https://git.callpipe.com/finn/signald) project, which in turn\nis a command-line client for the Signal messaging service.\n\npysignald allows you to programmatically send and receive messages to Signal.\n\nInstallation\n------------\n\nYou can install pysignald with pip:\n\n```\n$ pip install pysignald\n```\n\n\nRunning\n-------\n\nJust make sure you have signald installed. Here\'s an example of how to use pysignald:\n\n\n```python\nfrom signald import Signal\n\ns = Signal("+1234567890")\ns.send_message("+1098765432", "Hello there!")\n\nfor message in s.receive_messages():\n    print(message)\n```\n',
    'author': 'Stavros Korokithakis',
    'author_email': 'hi@stavros.io',
    'url': 'https://gitlab.com/stavros/pysignald/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
