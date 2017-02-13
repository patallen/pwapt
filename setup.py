from setuptools import setup, find_packages

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='PWAPT',
    version='0.0.1',
    description='Python Web Application Profiling Toolkit',
    long_description=long_description,
    url='https://github.com/patallen/pwapt',
    author='Patrick Allen',
    author_email='prallen90@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='profiling python web flamegraph',
    packages=find_packages(exclude=['docs', 'tests', 'dist']),
)
