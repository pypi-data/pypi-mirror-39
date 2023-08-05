from setuptools import setup

setup(name='Timetrap Youtrack',
      version='0.1',
      description='Timetrap youtrack terminal command for sending your worktime to youtrack',
      url='https://github.com/GranderStark/Timetrap-Youtrack',
      author='Lev Subbotin',
      author_email='grander.stark@yandex.ru',
      license='Apache 2.0',
      zip_safe=False,
      packages=[
          'timetrap_youtrack_package'
      ],
      package_dir={'': 'package'},
      scripts=['package/timetrap_youtrack_package/timetrap_youtrack'],
      install_requires=[
          'requests',
          'marshmallow',
          'certifi',
          'chardet',
          'dictknife',
          'idna',
          'importlib2',
          'magicalimport',
          'marshmallow',
          'prestring',
          'Python3-Youtrack-api',
          'PyYAML',
          'requests',
          'SQLAlchemy',
          'toml',
          'urllib3'
      ],
      )
