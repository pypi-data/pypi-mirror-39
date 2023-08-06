# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['bavaria', 'bavaria.api']

package_data = \
{'': ['*']}

install_requires = \
['websockets>=7.0,<8.0']

setup_kwargs = {
    'name': 'bavaria',
    'version': '0.1.0',
    'description': "API wrapper for Munich's unoffical S-Bahn websocket API.",
    'long_description': None,
    'author': 'Auke Willem Oosterhoff',
    'author_email': 'auke@orangetux.nl',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
