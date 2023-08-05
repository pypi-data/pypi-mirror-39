'''
Install script for biomap-miriam
'''

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='biomap-miriam',
    version='0.0.52',
    author='Sebastian Winkler',
    author_email='winkler@informatik.uni-tuebingen.de',
    description='BioMap MIRIAM (Identifiers.org) mapper',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BioMapOrg/biomap-miriam',
    packages=setuptools.find_packages(),
    install_requires=[
        'biomap-utils>=0.0.51',
        'jsonschema==2.6.0',
        'PyYAML',
        'lxml',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
    ]
)
