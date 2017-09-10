from setuptools import setup

requires = [
    'pyramid',
    'pyramid_jinja2',
    # deform, will also install colander
    'deform>=2.0a2',
    'pyramid_sqlalchemy',
    # each web request is handled as a transaction,
    # incoming request starts and transaction and an out going request ends a trasaction
    # if nothing goes wrong all integrated dbs commit their work
    # 'any error' anywhere will abort the transaction
    'pyramid_tm'
]
setup(name='mysite',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = mysite:main
      [console_scripts]
      initialize_db = mysite.scripts.initialize_db:main
      """
      # the line above will initialize this script in our virtual enviroments bin directory
      # this will generate a simple python file, which is wrapped around our specific callable
      )
