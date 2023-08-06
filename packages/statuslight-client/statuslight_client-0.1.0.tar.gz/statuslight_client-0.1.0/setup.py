# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['statuslight_client']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.4,<4.0']

setup_kwargs = {
    'name': 'statuslight-client',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Bengtsson',
    'author_email': 'daniel.f.bengtsson@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
