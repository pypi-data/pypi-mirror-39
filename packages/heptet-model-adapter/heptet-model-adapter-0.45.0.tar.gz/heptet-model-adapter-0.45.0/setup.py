from setuptools import setup, find_packages

requires = ['heptet-app', 'db-dump', 'lxml']

setup(name='heptet-model-adapter',
      version='0.45.0',
      packages=find_packages(),
      install_requires=requires,
      )