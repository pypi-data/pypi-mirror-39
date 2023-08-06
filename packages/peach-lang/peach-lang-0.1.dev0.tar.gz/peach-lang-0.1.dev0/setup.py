from distutils.core import setup
from setuptools import find_packages

setup(
    name='peach-lang',
    version='0.1dev',
    packages=find_packages(exclude=('tests',)),
    license='',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)