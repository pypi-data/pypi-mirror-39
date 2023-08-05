# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aiosql', 'aiosql.loaders']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiosql',
    'version': '0.1.1',
    'description': 'Simple SQL in Python.',
    'long_description': '# aiosql\n\nSimple SQL in Python\n\nBased on the wonderful [anosql](https://github.com/honza/anosql) library, which is in turn based on the excellent clojure library [Yesql](https://github.com/krisajenkins/yesql/) by Kris Jenkins.\n\nExciting features of `aiosql`:\n \n 1. Out of the box support for [`asyncio`](https://docs.python.org/3/library/asyncio.html) based database drivers like [aiosqlite](https://github.com/jreese/aiosqlite) and [asyncpg](https://github.com/MagicStack/asyncpg).\n 2. Load nested directories `.sql` files.\n 3. Easy extension to accommodate custom database drivers.\n\n## Install\n\nTODO\n\n## Usage\n\n### Basics\n\nGiven a `greetings.sql` file:\n\n```sql\n-- name: get-all-greetings\n-- Get all the greetings in the database\nselect * from greetings;\n\n-- name: $get-users-by-username\n-- Get all the users from the database,\n-- and return it as a dict\nselect * from users where username = :username;\n```\n\nWith the stdlib `sqlite3` driver built into python you can use this sql file:\n\n```python\nimport sqlite3\nimport aiosql\n\nqueries = aiosql.from_path("greetings.sql", db_driver="sqlite3")\nconn = sqlite3.connect("greetings.db")\n\n# greetings = [(1, "Hi"), (2, "Aloha"), (3, "Hola")]\n# users = [{"user_id": 1, "username": "willvaughn", "name": "Will"}]\ngreetings = queries.get_greetings(conn)\nusers = queries.get_users_by_username(conn, username="willvaughn")\n\n\nname = users[0]["name"]\nfor _, greeting in greetings:\n    print(f"{greeting}, {name}!")\n\n# Hi, Will!\n# Aloha, Will!\n# Hola, Will!\n```\n\nTo do this in an asyncio environment you can use the [aiosqlite](https://github.com/jreese/aiosqlite) driver.\n\n```python\nimport asyncio\n\nimport aiosql\nimport aiosqlite\n\n\nasync def main():\n    queries = aiosql.from_path("greetings.sql", db_driver="aiosqlite")\n\n    # Parallel queries!!!\n    with async aiosqlite.connect("greetings.db") as conn:\n        greetings, users = await asyncio.gather(\n            queries.get_all_greetings(conn),\n            queries.get_users_by_username(conn, username="willvaughn")\n        )\n        \n    # greetings = [(1, "Hi"), (2, "Aloha"), (3, "Hola")]\n    # users = [{"user_id": 1, "username": "willvaughn", "name": "Will"}]\n    name = users[0]["name"]\n    for _, greeting in greetings:\n        print(f"{greeting}, {name}!")\n        \n    # Hi, Will!\n    # Aloha, Will!\n    # Hola, Will!\n    \n\nasyncio.run(main())\n```\n',
    'author': 'William Vaughn',
    'author_email': 'vaughnwilld@gmail.com',
    'url': 'https://gitlab.com/willvaughn/aiosql',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
