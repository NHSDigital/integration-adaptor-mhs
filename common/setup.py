from setuptools import setup, find_packages

setup(
    name='integration-adaptors-common',
    version='',
    packages=find_packages(),
    url='https://github.com/nhsconnect/integration-adaptor-common',
    license='',
    author='NIA Development Team',
    author_email='',
    description='Common utilities used by the NHS integration adaptors projects.',
    install_requires=[
        'pystache~=0.5',
        'lxml~=4.4',
        'python-qpid-proton~=0.28',
        'tornado~=6.0',
        'isodate~=0.6',
        'aioboto3~=8.0',
        'motor~=2.1'
    ]
)
