from setuptools import setup

setup(name='kfet_server',
      version='0.1',
      description="Serveur web du site de la kfet de l'ENS de Lyon",
      url='http://github.com/shhun/kfet',
      author='shhun',
      install_requires=[
          'passlib',
          'flask',
      ],
      zip_safe=False)

