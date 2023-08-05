'''
Install script for biomap-utils
'''

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='biomap-utils',
    version='0.0.50',
    author='Sebastian Winkler',
    author_email='winkler@informatik.uni-tuebingen.de',
    description='BioMap utilities',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/BioMapOrg/biomap-utils',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ]
)
