# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['starlette_api', 'starlette_api.codecs', 'starlette_api.components']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>2', 'starlette>=0.9.0']

setup_kwargs = {
    'name': 'starlette-api',
    'version': '0.1.8',
    'description': 'Starlette API layer inherited from APIStar',
    'long_description': "# Starlette API\n[![Build Status](https://travis-ci.org/PeRDy/starlette-api.svg?branch=master)](https://travis-ci.org/PeRDy/starlette-api)\n[![codecov](https://codecov.io/gh/PeRDy/starlette-api/branch/master/graph/badge.svg)](https://codecov.io/gh/PeRDy/starlette-api)\n[![PyPI version](https://badge.fury.io/py/starlette-api.svg)](https://badge.fury.io/py/starlette-api)\n\n* **Version:** 0.1.8\n* **Status:** Production/Stable\n* **Author:** José Antonio Perdiguero López\n\n## Features\n\nThat library aims to bring a layer on top of Starlette framework to provide useful mechanism for building APIs. It's \nbased on API Star, inheriting some nice ideas like:\n\n* **Schema system** based on [Marshmallow](https://github.com/marshmallow-code/marshmallow/) that allows to **declare**\nthe inputs and outputs of endpoints and provides a reliable way of **validate** data against those schemas.\n* **Dependency Injection** that ease the process of managing parameters needed in endpoints.\n* **Components** as the base of the plugin ecosystem, allowing you to create custom or use those already defined in \nyour endpoints, injected as parameters.\n* **Starlette ASGI** objects like `Request`, `Response`, `Session` and so on are defined as components and ready to be \ninjected in your endpoints.\n\n## Credits\n\nThat library started mainly as extracted pieces from [APIStar](https://github.com/encode/apistar) and adapted to work \nwith [Starlette](https://github.com/encode/starlette).\n",
    'author': 'José Antonio Perdiguero López',
    'author_email': 'perdy@perdy.io',
    'url': 'https://github.com/PeRDy/starlette-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
