# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kangaroo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'kangaroo',
    'version': '0.1.0',
    'description': 'Find the absolute path of the desired file in parent directories.',
    'long_description': '# Kangaroo\n',
    'author': 'Fatih Sarhan',
    'author_email': 'f9n@protonmail.com',
    'url': 'https://github.com/f9n/kangaroo',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
