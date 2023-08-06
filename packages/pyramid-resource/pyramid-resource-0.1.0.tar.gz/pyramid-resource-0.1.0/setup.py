# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['pyramid_resource']
setup_kwargs = {
    'name': 'pyramid-resource',
    'version': '0.1.0',
    'description': 'A simple base resource class for Pyramid traversal.',
    'long_description': '# pyramid-resource\n\nA base resource class for Pyramid traversal.\n',
    'author': 'Theron Luhn',
    'author_email': 'theron@luhn.com',
    'url': 'https://github.com/luhn/pyramid-resource',
    'py_modules': modules,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
