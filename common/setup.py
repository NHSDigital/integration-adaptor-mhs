from distutils.core import setup

import setuptools

setup(
    name='integration-adaptors-common',
    version='0.1',
    packages=setuptools.find_packages(),
    url='https://digital.nhs.uk/developer/api-catalogue/mhs',
    license='Apache License, Version 2.0',
    author='Gareth Allan',
    author_email='niasupport@nhs.net',
    description='Common utilities used by the NHS integration adaptors projects.',
    install_requires=[
        'pystache',
        'lxml'
    ]
)
