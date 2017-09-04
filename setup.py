from setuptools import setup

requires = [
    'pyramid',
    'pyramid_jinja2',
    # deform, will also install colander
    'deform>=2.0a2'
]
setup(name='mysite',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = mysite:main
      """
      )
