# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['url_checks']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-url-checks',
    'version': '0.2.0',
    'description': 'Django checks to ensure valid URL Configurations',
    'long_description': '[![PyPI Version](https://img.shields.io/pypi/v/django-url-checks.svg)](https://pypi.org/project/django-url-checks/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/django-url-checks.svg)](https://pypi.org/project/django-url-checks/)\n[![Django Versions](https://img.shields.io/pypi/djversions/django-url-checks.svg)](https://pypi.org/project/django-url-checks/)\n[![Build Status](https://travis-ci.org/jambonsw/django-url-checks.svg?branch=development)](https://travis-ci.org/jambonsw/django-url-checks)\n[![codecov](https://codecov.io/gh/jambonsw/django-url-checks/branch/development/graph/badge.svg)](https://codecov.io/gh/jambonsw/django-url-checks)\n[![BCH compliance](https://bettercodehub.com/edge/badge/jambonsw/django-url-checks?branch=development)](https://bettercodehub.com/)\n\n# Read Me\n\nUse Django\'s System Check Framework to ensure your URL Configuration\nworks correctly.\n\n## Table of Contents\n\n- [Project Purpose](#project-purpose)\n- [Project Rationale](#project-rationale)\n- [Installation and Usage](#installation-and-usage)\n- [Contributing](#contributing)\n\n## Project Purpose\n\nThis package checks your Django project\'s URL Configuration for a few\nthings.\n\n- Do the paths or regular expressions in your URL configuration tree end\n  with slashes (or, for regular expressions, `/$`)\n- Is the URL configuration tree comprised of only `URLPattern` and\n  `URLResolver` instances (`path()` and `include()`)?\n- Is `ROOT_URLCONF` defined in settings, and does it point to a valid\n  Python module with `urlpatterns` defined?\n\n[🔝 Up to Table of Contents](#table-of-contents)\n\n## Project Rationale\n\nI constantly forget to add a slash to the end of my URI paths. This\nleads to strange behavior, and can be tricky to catch even with proper\ntesting.\n\nWhat\'s more, the errors raised when something is amiss with the URL\nconfiguration can be tricky to debug and understand.\n\nAs such, this package aim to try and make developers lives easier by\nproviding targeted checks of the URL configuration tree. This is meant\nto be used as part of a "belt-and-braces" approach, and is not a\nsubstitution for tests!\n\nI am open to suggestions on improving the checks. Please open an issue\nto do so.\n\n[🔝 Up to Table of Contents](#table-of-contents)\n\n## Installation and Usage\n\n1. Add `"url_checks.apps.UrlChecksConfig",` as an item in your Django\n   project\'s `INSTALLED_APPS` setting\n2. In the terminal (in your Django projects code-root directory), run\n   Django\'s check framework with `$ python manage.py check`\n3. Read the output in your terminal and track those bugs down!\n\n🎉\n\n[🔝 Up to Table of Contents](#table-of-contents)\n\n## Contributing\n\nFor ideas, bugs, feature-requests, and all the rest, please open an\n[issue on Github](https://github.com/jambonsw/django-url-checks/issues).\n\n[🔝 Up to Table of Contents](#table-of-contents)\n',
    'author': 'Andrew Pinkham',
    'author_email': 'code@andrewsforge.com',
    'url': 'https://github.com/jambonsw/django-url-checks',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
