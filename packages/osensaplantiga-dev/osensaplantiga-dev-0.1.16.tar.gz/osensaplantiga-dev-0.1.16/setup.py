# Upload command:
# python setup.py sdist bdist_wheel upload [-r pypitest] (if .pypirc setup)
# python setup.py sdist bdist_wheel upload [-r https://test.pypi.org/legacy/]
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.txt'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='osensaplantiga-dev',
    packages=find_packages(),
    install_requires=['pyserial', 'python-dateutil', 'xmodem', 'fastavro'],
    python_requires='>=3.6',
    version='0.1.16',
    description='OSENSA-Plantiga Python library',
    long_description=long_description,
    author='OSENSA Innovations',
    author_email='cng@osensa.com',
    license='MIT',
    keywords=[],
    classifiers=[],
)
