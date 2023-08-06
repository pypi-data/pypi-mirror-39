# coding: utf-8

try:
    import setuptools
    from setuptools import setup, find_packages
except ImportError:
    print("Please install setuptools.")

setup(
    name  = 'imba',
    version = '0.0.4',
    license = 'MIT',
    author = 'hiroyam',
    author_email = 'hogehoge@gmail.com',
    url = 'https://github.com/hiroyam/imba',
    packages = find_packages(),
    install_requires = ['sklearn', 'pandas'],
)
