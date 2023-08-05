from setuptools import setup

setup(name='Python3-Youtrack-api',
      version='0.2',
      description='Python3 Youtrack api',
      url='https://github.com/GranderStark/Python3-Youtrack-api',
      author='Lev Subbotin',
      author_email='grander.stark@yandex.ru',
      license='Apache 2.0',
      zip_safe=False,
      packages=[
          'python3_youtrack_api'
      ],
      package_dir={'': 'package'},
      install_requires=[
          'requests',
          'marshmallow',
      ],
      )
