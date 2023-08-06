# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jrpygcloudml', 'jrpygcloudml.datasets']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'jrpygcloudml',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Colin',
    'author_email': 'colin@jumpingrivers.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
