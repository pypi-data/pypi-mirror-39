# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['formation']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=18.2,<19.0',
 'cytoolz>=0.9.0,<0.10.0',
 'requests>=2.20,<3.0',
 'toolz>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'formation',
    'version': '0.1.12',
    'description': 'A generic functional middleware infrastructure for Python.',
    'long_description': '![](media/cover.png)\n\n# Formation\n\nA generic functional middleware infrastructure for Python.\n\nTake a look:\n\n```py\nfrom datetime.datetime import now\nfrom formation import wrap\nfrom requests import get\n\ndef log(ctx, call):\n    print("started")\n    ctx = call(ctx)\n    print("ended")\n    return ctx\n\ndef timeit(ctx, call):\n    started = now()\n    ctx = call(ctx)\n    ended = now() - started\n    ctx[\'duration\'] = ended\n    return ctx\n\ndef to_requests(ctx):\n    get(ctx[\'url\'])\n\nfancy_get = wrap(to_requests, middleware=[log, timeit])\nfancy_get({\'url\':\'https://google.com\'})\n```\n\n## Quick Start\n\nInstall using pip/pipenv/etc. (we recommend [poetry](https://github.com/sdispater/poetry) for sane dependency management):\n\n```\n$ poetry add formation\n```\n\n### Thanks:\n\nTo all [Contributors](https://github.com/jondot/formation/graphs/contributors) - you make this happen, thanks!\n\n# Copyright\n\nCopyright (c) 2018 [@jondot](http://twitter.com/jondot). See [LICENSE](LICENSE.txt) for further details.',
    'author': 'Dotan Nahum',
    'author_email': 'jondotan@gmail.com',
    'url': 'https://github.com/jondot/formation',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
}


setup(**setup_kwargs)
