# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='tkh_dnsr_pipeline_v00.00.01',
    version='00.00.01',
    description='First Pip packaged attempt at testing the TKH custom built Data Storage and Retrieval Pipeline.',
    long_description=readme,
    author='Sean Gies, Niek Derksen, Denis Karakoç, Okko Kruyssen, Pelle Kools and Bram Jodies',
    author_email='derksen394@gmail.com',
    url='https://gitlab.socsci.ru.nl/msdt/team1920-datastorage/tree/master',
    license=license,
    #packages=['tkh_dsnr_pipeline']
    packages=setuptools.find_packages(),
    install_requires = ['google-cloud-storage', 'certifi', 'wincertstore']
)


