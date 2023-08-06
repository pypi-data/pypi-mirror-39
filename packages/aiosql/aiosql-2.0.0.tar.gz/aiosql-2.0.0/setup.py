# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiosql', 'aiosql.adapters']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiosql',
    'version': '2.0.0',
    'description': 'Simple SQL in Python.',
    'long_description': "# aiosql\n\nSimple SQL in Python.\n\nSQL is code, you should be able to write it, version control it, comment on it, and use it in database tools\nlike `psql` as you would any other SQL. But, you also want to be able to use it from your python\napplications, and that's where `aiosql` can help. With `aiosql` you can organize your SQL statements in `.sql`\nfiles and load them into a python object as methods to call.\n\nThis project supports sync and asyncio based drivers for SQLite (`sqlite3`, `aiosqlite`) and PostgreSQL\n(`psycopg2`, `asyncpg`) out of the box, and can be extended to support other database drivers by you! The ``asyncio``\nsupport restricts this package to python versions >3.6. If you are using older versions of python please see the\nrelated [anosql](https://github.com/honza/anosql) package which this project is based on.\n\n## Install\n\n```\npip install aiosql\n```\n\nOr if you you use [poetry](https://poetry.eustace.io/):\n\n```\npoetry add aiosql\n```\n\n## Documentation\n\nProject and API docs https://nackjicholson.github.io/aiosql\n",
    'author': 'William Vaughn',
    'author_email': 'vaughnwilld@gmail.com',
    'url': 'https://gitlab.com/willvaughn/aiosql',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
