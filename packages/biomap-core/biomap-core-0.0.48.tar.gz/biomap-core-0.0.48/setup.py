'''
Install script for biomap-core
'''

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='biomap-core',
    version='0.0.48',
    author='Sebastian Winkler',
    author_email='winkler@informatik.uni-tuebingen.de',
    description='BioMap core interfaces',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BioMapOrg/biomap-core',
    packages=['biomap.core'],
    data_files=[
        ('schema', ['schema/mapper_definition_schema.json'])
    ],
    install_requires=[
        'jsonschema==2.6.0',
        'PyYAML'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent"
    ]
)
