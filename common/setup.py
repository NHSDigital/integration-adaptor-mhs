from setuptools import setup, find_packages

setup(
    name='integration-adaptors-common',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/nhsconnect/integration-adaptor-common',
    license='Apache License version 2.0',
    author='NIA Development Team',
    author_email='niasupport@nhs.net',
    description='Common utilities used by the NHS integration adaptors projects.',
    install_requires=[
        'pystache',
        'lxml',
        'python-qpid-proton',
        'tornado',
        'isodate',
        'aioboto3',
        'motor'
    ]
)