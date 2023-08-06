# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dikicli']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4']

entry_points = \
{'console_scripts': ['diki = dikicli.cli:main']}

setup_kwargs = {
    'name': 'dikicli',
    'version': '0.3.1',
    'description': 'Commandline interface to diki.pl polish-english dictionary.',
    'long_description': '# dikicli\n\nCommandline interface to diki.pl polish-english dictionary.\n\nDikicli allows you to use diki.pl from comfort of your terminal.\nAll results are cached for faster retrieval in the future.\n\n## Usage:\n\nTranslate english to polish:\n\n    diki word\n\nTranslate polish to engish:\n\n    diki -p word\n\nDisplay html file of all words translated so far:\n\n    diki -i\n',
    'author': 'Dawid Zych',
    'author_email': 'dawid.zych@yandex.com',
    'url': 'https://github.com/silenc3r/dikicli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
