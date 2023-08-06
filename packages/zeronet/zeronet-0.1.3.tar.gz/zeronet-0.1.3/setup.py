# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zeronet', 'zeronet.core', 'zeronet.utils']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.15,<2.0']

setup_kwargs = {
    'name': 'zeronet',
    'version': '0.1.3',
    'description': 'A Build-from-Scratch Example of Neural Network Learning Model based on NumPy.',
    'long_description': None,
    'author': 'ddlee',
    'author_email': 'cnlijiacheng96@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
