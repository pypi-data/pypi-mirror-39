# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['syllapy']

package_data = \
{'': ['*']}

install_requires = \
['ujson>=1.35,<2.0']

setup_kwargs = {
    'name': 'syllapy',
    'version': '0.7.0',
    'description': 'Calculate syllable counts for English words.',
    'long_description': 'SyllaPy\n=======\n\n<p>\n  <a href="https://badge.fury.io/py/syllapy"><img src="https://badge.fury.io/py/syllapy.svg" alt="PyPI version"></a>\n  <a href="https://travis-ci.org/mholtzscher/syllapy"><img src="https://travis-ci.org/mholtzscher/syllapy.svg?branch=master" alt="Travis CI"></a>\n  <a href="https://github.com/mholtzscher/syllapy"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black"></a>\n  <a href="https://codecov.io/gh/mholtzscher/syllapy">\n  <img src="https://codecov.io/gh/mholtzscher/syllapy/branch/master/graph/badge.svg" alt="Codecov"/></a>\n</p>\n\nCalculate syllable counts for English words.\n\n\nInstallation\n------------\n\n``` {.sourceCode .python}\npip install syllapy\n```\n\nUsage\n-----\n\n``` {.sourceCode .python}\nimport syllapy\ncount = syllapy.count(\'additional\')\n```\n\n',
    'author': 'Michael Holtzscher',
    'author_email': 'mholtz@protonmail.com',
    'url': 'https://github.com/mholtzscher/syllapy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
