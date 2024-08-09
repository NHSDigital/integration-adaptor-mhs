from distutils.core import setup

import setuptools

setup(
    name='scr',
    version='0.1',
    packages=setuptools.find_packages(),
    url='https://digital.nhs.uk/services/summary-care-records-scr',
    license='Apache version 2.0',
    author='Phillip Woods',
    author_email='niasupport@nhs.net',
    description='Artifacts for producing SCR requests.',
)