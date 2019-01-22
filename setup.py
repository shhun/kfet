from setuptools import setup

setup(name='kfet',
      version='0.1',
      description="Site de la kfet de l'ENS de Lyon",
      url='http://github.com/shhun/kfet',
      author='shhun',
      install_requires=[
          'websockets',
          'watchdogs',
          'passlib',
          'flask',
      ],
      zip_safe=False)

