# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiosql', 'aiosql.loaders']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiosql',
    'version': '1.0.0',
    'description': 'Simple SQL in Python.',
    'long_description': "# aiosql\n\nSimple SQL in Python.\n\nSQL is code, you should be able to write it, version control it, comment on it, and use it in database tools\nlike `psql` as you would any other SQL. But, you also want to be able to use it from your python\napplications, and that's where `aiosql` can help. With `aiosql` you can organize your SQL in `.sql`\nfiles and load them into a python object with methods to call.\n\nThe project is based on (and closely related to) the python package [anosql](https://github.com/honza/anosql), which\nis based on the clojure library [Yesql](https://github.com/krisajenkins/yesql/). It supports sync and asyncio\ndrivers for SQLite and PostgreSQL out of the box, and can be extended by you to support other database drivers!\n\n## Install\n\n```\npip install aiosql\n```\n\nOr if you you use [poetry](https://poetry.eustace.io/):\n\n```\npoetry add aiosql\n```\n\n## Documentation\n\nProject and API docs https://nackjicholson.github.io/aiosql\n",
    'author': 'William Vaughn',
    'author_email': 'vaughnwilld@gmail.com',
    'url': 'https://gitlab.com/willvaughn/aiosql',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
