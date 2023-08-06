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
 'structlog>=18.2,<19.0']

extras_require = \
{'torch': ['torch==1.0.0']}

entry_points = \
{'console_scripts': ['gcgc = gcgc.cli:main']}

setup_kwargs = {
    'name': 'gcgc',
    'version': '0.3.0',
    'description': 'GCGC is a preprocessing library for biological sequence model development.',
    'long_description': '# GCGC\n\n> GCGC is a python package for feature processing on Biological Sequences.\n\n[![](https://img.shields.io/pypi/v/gcgc.svg)](https://pypi.python.org/pypi/gcgc)\n[![](https://img.shields.io/travis/tshauck/gcgc.svg)](https://travis-ci.org/tshauck/gcgc)\n\n## Installation\n\nInstall GCGC via pip:\n\n```sh\n$ pip install gcgc\n```\n\nIf you\'d like to use one of the third party tools, install the related "extras".\n\n```bash\n$ pip install gcgc -E torch\n```\n\n## Documentation\n\nThe GCGC documentation is at [gcgc.trenthauck.com](http://gcgc.trenthauck.com).\n\n## Development Board\n\nThe GCGC development board is hosted on [notion](https://www.notion.so/3649815c53324f01ae03abc99707dc68?v=98d8b29c39544dca9cde8ddc0dd8c98b).\n',
    'author': 'Trent Hauck',
    'author_email': 'trent@trenthauck.com',
    'url': 'http://gcgc.trenthauck.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
