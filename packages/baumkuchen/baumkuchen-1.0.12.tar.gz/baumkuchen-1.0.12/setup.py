# coding: utf-8

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

setup(
    name  = 'baumkuchen',
    version = '1.0.12',
    license = 'MIT',
    author = 'hiroyam',
    author_email = 'hogehoge@gmail.com',
    url = 'https://github.com/hiroyam/baumkuchen',
    packages = find_packages(),
    install_requires = ['numpy','pandas'],
)
