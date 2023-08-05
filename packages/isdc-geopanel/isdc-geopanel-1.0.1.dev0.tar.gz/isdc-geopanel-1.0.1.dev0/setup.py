import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'VERSION')) as version_file:
    version = version_file.read().strip()

setup(
    name='isdc-geopanel',
    version= version,
    description='panel module',
    long_description=open(os.path.join(here, 'README.md')).read(),
    license='iMMAP',
    author ='iMMAP',
    author_email = 'asdc@immap.org',
    packages=find_packages(),
    include_package_data = True,
    install_requires=[],
    zip_safe= False
)
