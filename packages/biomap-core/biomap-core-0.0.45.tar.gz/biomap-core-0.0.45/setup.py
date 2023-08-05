'''
Install script for biomap-core
'''

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='biomap-core',
    version='0.0.45',
    author='Sebastian Winkler',
    author_email='winkler@informatik.uni-tuebingen.de',
    description='BioMap core interfaces',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BioMapOrg/biomap-core',
    packages=['biomap.core', 'biomap'],
    data_files=[
        ('schema', ['schema/mapper_definition_schema.json'])
    ],
    install_requires=[
        'jsonschema',
        'PyYAML'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
    ]
)
