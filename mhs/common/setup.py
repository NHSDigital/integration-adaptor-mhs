from distutils.core import setup

import setuptools

setup(
    name='mhs-common',
    packages=setuptools.find_packages(),
    url='',
    license='',
    author='',
    author_email='',
    description='Common utilities used by the NHS integration adaptors projects.',
    install_requires=[
        'defusedxml~=0.6',
        'aioboto3~=11.3',
        'tornado~=6.0',
        'isodate~=0.6',
        'marshmallow~=3.2',
    ]
)
