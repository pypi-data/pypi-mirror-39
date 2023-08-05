#!/usr/bin/env python
# coding: utf-8

import os
import sys
from setuptools import setup, find_packages
import incolumepy.clinica as package


if sys.argv[-1] == "dist":
    os.system("python setup.py bdist_wheel bdist_egg sdist --format zip,gztar")
    sys.exit()


if sys.argv[-1] == "publish":
    os.system("twine upload dist/incolumepy.clinica-{}*.whl".format(package.__version__))
    os.system("twine upload dist/incolumepy.clinica-{}*.egg".format(package.__version__))
    os.system("twine upload dist/incolumepy.clinica-{}*.tar.gz".format(package.__version__))
    sys.exit()


NAME = package.__package__
NAMESPACE = NAME.split('.')[:0]
DESCRIPTION = "pacote {}".format(NAME)
KEYWORDS = 'python incolumepy'
AUTHOR = '@britodfbr'
AUTHOR_EMAIL = 'contato@incolume.com.br'
URL = 'http://www.incolume.com.br'
PROJECT_URLS = {
    'Documentation': 'https://gitlab.com/development-incolume/{}/wikis/home'.format(NAME),
    'Funding': None,
    'Say Thanks!': None,
    'Source': 'https://gitlab.com/development-incolume/{}'.format(NAME),
    'Git prod': 'https://gitlab.com/development-incolume/{}.git'.format(NAME),
    'Git dev': 'https://gitlab.com/clinicaesteticabrito/{}.git'.format(NAME),
    'Tracker': 'https://gitlab.com/clinicaesteticabrito/{}/issues'.format(NAME),
    'Oficial': 'https://pypi.org/project/{}/'.format(NAME),
}
LICENSE = 'BSD'
# Get more strings from https://pypi.org/classifiers
CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    # 'Development Status :: 5 - Production/Stable',
    'Operating System :: OS Independent',
    'Natural Language :: Portuguese (Brazilian)',
    "Programming Language :: Python",
    'Topic :: Software Development :: Libraries :: Python Modules',
    'Topic :: Utilities'
]


with open('README.md')as f:
    readme = f.read()
with open(os.path.join("docs", "HISTORY.rst")) as f:
    history = f.read()
with open('CONTRIBUTING.md') as f:
    contibutors = f.read()
with open('CHANGELOG') as f:
    changes = f.read()

VERSION = package.__version__
LONG_DESCRIPTION = '\n\n'.join((
    readme,
    history,
    contibutors,
    changes))

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,

      classifiers=CLASSIFIERS,
      keywords=KEYWORDS,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      url=URL,
      project_urls=PROJECT_URLS,
      license=LICENSE,
      namespace_packages=NAMESPACE,
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      test_suite='nose.collector',
      tests_require='nose',
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'gspread',
          'oauth2client',
      ],
      entry_points={
          'console_scripts': [
              'version =  incolumepy.clinica:version',
              'package = incolumepy.clinica:package'
          ],
          'gui_scripts': [
              'baz = my_package_gui:start_func',
          ],
      },

      # entry_points="""
      # -*- Entry points: -*-

      # [distutils.setup_keywords]
      # paster_plugins = setuptools.dist:assert_string_list

      # [egg_info.writers]
      # paster_plugins.txt = setuptools.command.egg_info:write_arg
      # """,
      # paster_plugins = [''],
      )
