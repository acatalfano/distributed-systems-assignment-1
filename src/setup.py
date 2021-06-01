from setuptools import setup, find_packages

setup(
    name='assignment 1',
    version='1.0.0',
    packages=find_packages(include=['app', 'app.*', 'test', 'test.*.*'])
)
