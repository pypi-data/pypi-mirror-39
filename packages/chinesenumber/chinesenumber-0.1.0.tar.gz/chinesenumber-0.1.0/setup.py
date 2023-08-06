# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['chinesenumber']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chinesenumber',
    'version': '0.1.0',
    'description': 'Convert Chinese (or Japanese) numbers to numeric digits (21)',
    'long_description': "# ChineseNumber\n\nConvert Chinese (or Japanese) numbers (e.g. \xe4\xba\x8c\xe5\x8d\x81\xe4\xb8\x80) to numeric digits (21).\n\nSimilar in idea to https://github.com/akshaynagpal/w2n\n\nThe resulting numbers can be sorted using https://github.com/SethMMorton/natsort\n\n## Usage\n\n```pydocstring\n>>> from chinesenumber import NumberParser\n>>> parser = NumberParser()\n>>> parser.numberify('\xe7\xac\xac\xe4\xba\x8c\xe5\x8d\x81\xe4\xba\x8c\xe8\xaf\xbe')\n'\xe7\xac\xac22\xe8\xaf\xbe'\n>>> parser.simple_parse('\xe7\x99\xbe\xe5\x85\xad\xe5\x8d\x81\xe4\xba\x94')\n165\n```\n\n## Installation\n\n```\npip install chinesenumber\n```\n",
    'author': 'Pacharapol Withayasakpunt',
    'author_email': 'patarapolw@gmail.com',
    'url': 'https://github.com/patarapolw/chinesenumber',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3',
}


setup(**setup_kwargs)
