import re
import os

from setuptools import setup, find_packages

package_name = 'the_metrix'

try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    requirements = []

try:
    with open(os.path.join(os.path.dirname(__file__), package_name, '__init__.py')) as f:
        version = re.search(r"__version__ = '(.*)'", f.read()).group(1)
except FileNotFoundError:
    version = 'test'

classifiers = [
    'Development Status :: 3 - Alpha',

    'Operating System :: OS Independent',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Science/Research',

    'License :: OSI Approved :: MIT License',

    'Natural Language :: English',

    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: Implementation :: CPython',

    'Topic :: Scientific/Engineering'
]

setup(
    name=package_name,
    packages=find_packages(),
    url='https://github.com/Ffisegydd/the_metrix',
    license='MIT',
    author='K J P',
    author_email='ffisegydd@ffisegydd.com',
    description='A set of functions for performing metrics analysis.',
    install_requirements=requirements,
    classifiers=classifiers,
    version=version
)