from distutils.core import setup

import setuptools

setup(
    name='integration-adaptors-common',
    version='',
    packages=setuptools.find_packages(),
    url='git@github.com:nhsconnect/integration-adaptor-common.git',
    license='',
    author='NIA Development Team',
    author_email='',
    description='Common utilities used by the NHS integration adaptors projects.',
    install_requires=[
        'pystache',
        'lxml',
        'python-qpid-proton',
        'tornado',
        'isodate'
    ]
)
