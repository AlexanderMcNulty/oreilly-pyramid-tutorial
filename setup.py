from setuptools import setup

requires = [
    'pyramid',
    'pyramid_sqlalchemy',
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
      )
