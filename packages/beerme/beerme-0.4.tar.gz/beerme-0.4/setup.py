from setuptools import setup, find_packages
import sys, os

version = '0.4'

setup(name='beerme',
      version=version,
      description="Untapped beer list scraper",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Jared Rodriguez',
      author_email='jared@blacknode.net',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          "beautifulsoup4",
          "requests"
      ],
      entry_points={
        'console_scripts': [
            'beerme=beerme.beerme:main'
        ]
      }
      )
