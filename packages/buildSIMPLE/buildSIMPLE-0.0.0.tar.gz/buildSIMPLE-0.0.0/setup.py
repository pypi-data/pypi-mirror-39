from setuptools import setup, find_packages


setup(
  name = 'buildSIMPLE',         
  packages = ['buildSIMPLE'],   
  version = '0.0.0',      
  license='Mozilla Public License, v. 2.0',        
  description = 'buildSIMPLE is an open-source project dedicated to the development and maintenance of a python library for building performance modeling with full built-in support for the bsim data model.',
  author = 'Sagar Rao',
  author_email = 'sagar.rao@neumodlabs.com',
  url = 'https://www.neumodlabs.com',
  download_url = 'https://github.com/neumodlabs/buildSIMPLE',
  keywords = ['building performance modeling', 'energyplus', 'equest', 'ccbec', 'energy modeling'],
  install_requires=[],
  classifiers=[
    'Development Status :: 1 - Planning',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)