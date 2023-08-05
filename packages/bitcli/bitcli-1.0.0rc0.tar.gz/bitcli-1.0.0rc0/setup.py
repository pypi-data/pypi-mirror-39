
from setuptools import setup, find_packages
from bitcli.core.version import get_version

VERSION = get_version()

f = open('README.md', 'r')
LONG_DESCRIPTION = f.read()
f.close()

setup(
    name='bitcli',
    version=VERSION,
    description='Show prices in the console from Bitpanda',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author='Julio Molina Soler',
    author_email='julio@molinasoler.xyz',
    url='https://github.com/jmolinaso/bitcli/',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'tests*']),
    package_data={'bitcli': ['templates/*']},
    include_package_data=True,
    entry_points="""
        [console_scripts]
        bitcli = bitcli.main:main
    """,
)
