
from setuptools import setup, find_packages
from cementstarter.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='cementstarter',
    version=VERSION,
    description='A cement boilerplate',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='create email',
    author_email='john.doe@example.com',
    url='https://github.com/johndoe/myapp/',
    license='unlicensed',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'cementstarter': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        cementstarter = cementstarter.main:main
    """,
)
