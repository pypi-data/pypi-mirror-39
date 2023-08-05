
from setuptools import setup, find_packages

from kontrctl.version import KONTRCTL_VERSION

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [ 'click', 'kontr-api', 'tabulate' ]

extras = {
          'dev': [
              'pytest',
              'coverage',
              'mock',
              ],
          'docs': ['sphinx']
          }
          
classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        ]


entry_points = {
          'console_scripts': [
              'kontrctl = kontrctl.cli:cli_main',
              ],
        }

setup(name='kontrctl',
      version=KONTRCTL_VERSION,
      description='Kontr portal CLI',
      author='Peter Stanko',
      author_email='stanko@mail.muni.cz',
      url='https://gitlab.fi.muni.cz/grp-kontr2/kontrctl',
      packages=find_packages(exclude=("tests",)),
      long_description=long_description,
      long_description_content_type='text/markdown',
      include_package_data=True,
      install_requires=requirements,
      extras_require=extras,
      entry_points= entry_points,
      classifiers=classifiers,
      )
