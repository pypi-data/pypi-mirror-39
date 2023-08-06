# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pytest-dicom',
    version='0.0.1a0',
    description='pytest plugin to provide DICOM fixtures',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/suever/pytest-dicom',
    author='Jonathan Suever',
    author_email='suever@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    keywords='pytest dicom testing',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['pydicom', 'pytest']
)
