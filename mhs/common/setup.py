from distutils.core import setup

import setuptools

setup(
    name='mhs-common',
    version='0.1',
    packages=setuptools.find_packages(),
    url='',
    license='Apache version 2.0',
    author='Philip Woods',
    author_email='niasupport@nhs.net',
    description='Common utilities used by the NHS integration adaptors projects.',
    install_requires=[
        'defusedxml~=0.6',
        'aioboto3~=8.0',
        'tornado~=6.0',
        'isodate~=0.6',
        'marshmallow~=3.2',
    ]
)
