# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['howoldru']
install_requires = \
['fire>=0.1.3,<0.2.0', 'pendulum>=2.0,<3.0']

entry_points = \
{'console_scripts': ['howoldru = howoldru:main']}

setup_kwargs = {
    'name': 'howoldru',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'kk6',
    'author_email': 'hiro.ashiya@gmail.com',
    'url': 'https://github.com/kk6',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
