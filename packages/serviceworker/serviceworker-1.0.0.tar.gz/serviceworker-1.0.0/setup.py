import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = []

message_extractors = {},

setup(name='serviceworker',
      version='1.0.0',
      description='serviceworker',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[],
      author='hemanjosko',
      author_email='',
      url='',
      keywords='serviceworker',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='serviceworker',
      install_requires=requires,
      entry_points='',
      )
