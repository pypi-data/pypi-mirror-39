from setuptools import find_packages, setup

setup(
    name='kompass',
    version='0.0.0.1',
    description='crawl the kompass',
    author='test',
    author_email='3168095199@qq.com',
    url='https://test.example.com',
    packages = find_packages(exclude=['docs', 'tests*']),
)