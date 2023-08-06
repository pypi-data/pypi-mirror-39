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
    'version': '0.1.0',
    'description': 'Django checks to ensure valid URL Configurations',
    'long_description': '# Read Me\n\nEven with proper testing, it\'s easy to accidentally forget a slash at\nthe end of a URI path in Django\'s URL configuration, which in turn can\nlead to unexpected behavior. This Django check helps follow a\nbelt-and-braces approach and will verify that all paths (endpoints and\nincludes) end with a slash (or, for regular expressions, `"/$"`).\n\nI am open to suggestions on improving the check. Please open an issue to\ndo so.\n',
    'author': 'Andrew Pinkham',
    'author_email': 'code@andrewsforge.com',
    'url': 'https://github.com/jambonsw/django-url-checks',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
