# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jrpyanalytics']

package_data = \
{'': ['*']}

install_requires = \
['graphviz>=0.10.1,<0.11.0',
 'matplotlib>=3.0,<4.0',
 'numpy>=1.15,<2.0',
 'pandas>=0.23.4,<0.24.0',
 'seaborn>=0.9.0,<0.10.0',
 'sklearn>=0.0.0,<0.0.1']

setup_kwargs = {
    'name': 'jrpyanalytics',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Jamie',
    'author_email': 'jamie@jumpingrivers.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
