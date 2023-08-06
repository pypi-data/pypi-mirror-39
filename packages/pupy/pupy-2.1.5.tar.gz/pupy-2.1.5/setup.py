# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['pupy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pupy',
    'version': '2.1.5',
    'description': 'pretty useful python',
    'long_description': None,
    'author': 'jessekrubin',
    'author_email': 'jessekrubin@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
