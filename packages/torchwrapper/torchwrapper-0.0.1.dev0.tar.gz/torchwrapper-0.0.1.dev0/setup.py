# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()
    
with open('requirements.txt', 'r') as f:
    reqs = f.read().split('\n')
    
setup(
    name='torchwrapper',
    version='0.0.1.dev0',
    description='A Wrapper for PyTorch Models',
    license='MIT',
    long_description=long_description,
    author='Jay Morgan',
    url='https://gitlab.com/jaymorgan/torchwrapper/',
    packages=['torchwrapper'],
    install_requires=reqs,
    long_description_content_type='text/markdown',
    include_package_data=True,
)
