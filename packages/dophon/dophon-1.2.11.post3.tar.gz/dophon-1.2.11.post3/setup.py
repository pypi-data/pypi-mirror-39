# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['dophon',
 'dophon.annotation',
 'dophon.annotation.req',
 'dophon.annotation.res',
 'dophon.def_prop',
 'dophon.logger',
 'dophon.properties',
 'dophon.tools']

package_data = \
{'': ['*']}

install_requires = \
['Flask_Bootstrap',
 'PyMySQL',
 'dophon-manager',
 'flask',
 'gevent',
 'pyyaml>=3.13,<4.0',
 'schedule',
 'urllib3']

setup_kwargs = {
    'name': 'dophon',
    'version': '1.2.11.post3',
    'description': 'dophon web framework like springboot',
    'long_description': None,
    'author': 'CallMeE',
    'author_email': 'ealohu@163.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
