# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['frisco_mazi']
install_requires = \
['click>=7.0,<8.0', 'xlsxwriter>=1.1,<2.0']

entry_points = \
{'console_scripts': ['frisco-mazi = frisco_mazi:main']}

setup_kwargs = {
    'name': 'frisco-mazi',
    'version': '0.2.0',
    'description': 'An idiosyncratic tool for parsing products list from Frisco confirmation e-mails',
    'long_description': None,
    'author': 'Tadek Teleżyński',
    'author_email': 'tadekte@gmail.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
