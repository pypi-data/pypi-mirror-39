# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['datafiles', 'datafiles.tests']

package_data = \
{'': ['*']}

install_requires = \
['cached_property>=1.5,<2.0',
 'classproperties>=0.1.3,<0.2.0',
 'minilog>=1.2.1,<2.0.0',
 'ruamel.yaml>=0.15.46,<0.16.0']

setup_kwargs = {
    'name': 'datafiles',
    'version': '0.1a5',
    'description': 'File-based ORM for dataclasses.',
    'long_description': '[![Build Status](https://travis-ci.org/jacebrowning/datafiles.svg?branch=master)](https://travis-ci.org/jacebrowning/datafiles)\n',
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'url': 'https://pypi.org/project/datafiles',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
