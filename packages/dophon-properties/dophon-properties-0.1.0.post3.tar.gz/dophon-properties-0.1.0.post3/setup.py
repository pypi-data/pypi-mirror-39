# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dophon_properties',
 'dophon_properties.main',
 'dophon_properties.mq',
 'dophon_properties.tools']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dophon-properties',
    'version': '0.1.0.post3',
    'description': 'dophon properties module',
    'long_description': None,
    'author': 'CallMeE',
    'author_email': 'ealohu@163.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
