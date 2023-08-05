# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['google_music_utils']

package_data = \
{'': ['*']}

install_requires = \
['audio-metadata>=0.2,<0.3', 'multidict>=4.0,<5.0', 'wrapt>=1.10,<2.0']

extras_require = \
{'dev': ['coverage>=4.5,<5.0',
         'flake8>=3.5,<4.0',
         'flake8-builtins>=1.0,<2.0',
         'flake8-import-order>=0.18,<0.19',
         'flake8-import-order-tbm>=1.0.0,<2.0.0',
         'pytest>=3.6,<4.0',
         'sphinx>=1.7,<2.0',
         'tox>=2.9,<3.0'],
 'doc': ['sphinx>=1.7,<2.0'],
 'lint': ['flake8>=3.5,<4.0',
          'flake8-builtins>=1.0,<2.0',
          'flake8-import-order>=0.18,<0.19',
          'flake8-import-order-tbm>=1.0.0,<2.0.0'],
 'test': ['coverage>=4.5,<5.0', 'pytest>=3.6,<4.0', 'tox>=2.9,<3.0']}

setup_kwargs = {
    'name': 'google-music-utils',
    'version': '1.1.1',
    'description': 'A set of utility functionality for google-music and related projects.',
    'long_description': '# google-music-utils\n\n[![Travis (.org)](https://img.shields.io/travis/thebigmunch/google-music-utils.svg)](https:/travis-ci.org/thebigmunch/google-music-utils)\n[![Codecov](https://img.shields.io/codecov/c/github/thebigmunch/google-music-utils.svg)](https://codecov.io/gh/thebigmunch/google-music-utils)\n[![Read the Docs](https://img.shields.io/readthedocs/google-music-utils.svg)](https://google-music-utils.readthedocs.io)\n\n\n[google-music-utils](https://github.com/thebigmunch/google-music-utils) is a\nset of utility functionality for google-music and related projects.\n\n\n## Installation\n\n``pip install google-music-utils``\n\n\n## Usage\n\nFor the release version, see the [stable docs](https://google-music-utils.readthedocs.io/en/stable/).  \nFor the development version, see the [latest docs](https://google-music-utils.readthedocs.io/en/latest/).\n\n\n## Appreciation\n\nShowing appreciation is always welcome.\n\n#### Thank\n\n[![Say Thanks](https://img.shields.io/badge/thank-thebigmunch-blue.svg?style=flat-square)](https://saythanks.io/to/thebigmunch)\n\nGet your own thanks inbox at [SayThanks.io](https://saythanks.io/).\n\n#### Contribute\n\n[Contribute](https://github.com/thebigmunch/google-music-utils/blob/master/.github/CONTRIBUTING.md) by submitting bug reports, feature requests, or code.\n\n#### Help Others/Stay Informed\n\n[Discourse forum](https://forum.thebigmunch.me/)\n\n#### Referrals/Donations\n\n[![Coinbase](https://img.shields.io/badge/Coinbase-referral-orange.svg?style=flat-square)](https://www.coinbase.com/join/52502f01e0fdd4d3ef000253) [![Digital Ocean](https://img.shields.io/badge/Digital_Ocean-referral-orange.svg?style=flat-square)](https://m.do.co/c/3823208a0597) [![Namecheap](https://img.shields.io/badge/Namecheap-referral-orange.svg?style=flat-square)](https://www.namecheap.com/?aff=67208) [![PayPal](https://img.shields.io/badge/PayPal-donate-brightgreen.svg?style=flat-square)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=DHDVLSYW8V8N4&lc=US&item_name=thebigmunch&currency_code=USD)\n\n**BTC:** ``1BMLCFPcX8YHE1He2t3aBrsNDGr1pKhfFa``  \n**ETH:** ``0x8E3f8d8eAedeA61Bf34A998A2104954FE508D5d0``  \n**LTC:** ``LgsQU1YaY4a4s7m9efjn6m35XhVEpW1xoP``\n',
    'author': 'thebigmunch',
    'author_email': 'mail@thebigmunch.me',
    'url': 'https://github.com/thebigmunch/google-music-utils',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
