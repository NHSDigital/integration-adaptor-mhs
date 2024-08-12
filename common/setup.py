from setuptools import setup, find_packages

setup(
    name='integration-adaptors-common',
    packages=find_packages(),
    url='https://github.com/nhsconnect/integration-adaptor-common',
    license='Apache 2.0',
    author='NIA Development Team',
    author_email='niasupport@nhs.net',
    description='Common utilities used by the NHS integration adaptors projects.',
    install_requires=[
        'pystache~=0.6',
        'lxml~=4.4',
        'python-qpid-proton~=0.28',
        'tornado~=6.0',
        'isodate~=0.6',
        'aioboto3~=11.3',
        'motor~=2.1'
    ]
)
