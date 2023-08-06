# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['gcgc',
 'gcgc.alphabet',
 'gcgc.data',
 'gcgc.datasets',
 'gcgc.encoded_seq',
 'gcgc.fields',
 'gcgc.parser',
 'gcgc.tests',
 'gcgc.tests.alphabet',
 'gcgc.tests.cli',
 'gcgc.tests.datasets',
 'gcgc.tests.encoded_seq',
 'gcgc.tests.fields',
 'gcgc.tests.fixtures',
 'gcgc.tests.parser',
 'gcgc.tests.third_party.pytorch_utils',
 'gcgc.third_party',
 'gcgc.third_party.pytorch_utils']

package_data = \
{'': ['*'],
 'gcgc.data': ['splice/*'],
 'gcgc.tests.fixtures': ['ecoli/*', 'p53_human/*']}

install_requires = \
['aiohttp>=3.4,<4.0',
 'biopython==1.72',
 'numpy==1.15.2',
 'structlog>=18.2,<19.0',
 'torch==1.0.0']

entry_points = \
{'console_scripts': ['gcgc = gcgc.cli:main']}

setup_kwargs = {
    'name': 'gcgc',
    'version': '0.2.4',
    'description': 'GCGC is a preprocessing library for biological sequence model development.',
    'long_description': None,
    'author': 'Trent Hauck',
    'author_email': 'trent@trenthauck.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
