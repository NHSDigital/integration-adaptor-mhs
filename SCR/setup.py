from distutils.core import setup

import setuptools

setup(
    name='scr',
    version='0.1',
    packages=setuptools.find_packages(),
    url='https://digital.nhs.uk/developer/api-catalogue/summary-care-record-hl7-v3',
    license='Apache License, Version 2.0',
    author='Phillip Woods',
    author_email='niasupport@nhs.net',
    description='Artifacts for producing SCR requests.',
)
