from setuptools import setup, find_packages
from os import path
from io import open

setup(
    name='baumkuchen',  # Required
    version='1.0.4',  # Required
    url='https://github.com/hiroyam/baumkuchen',  # Optional
    author='hiroyam',  # Optional
    author_email='hiroyam@users.noreply.github.com',  # Optional
    license='MIT',  # Optional
    packages=find_packages(),  # Required
    install_requires=['peppercorn'],  # Optional
)
