#coding=utf-8

from setuptools import setup, find_packages    
setup(
    name = 'rplugins',
    version = '0.0.1',
    keywords = ("plugins","pip","importlib","state"),
    description = "a plugin running system.",
    long_description = "a plugin running system.",
    license = "MIT Licence",
    url = "https://github.com/v1xingyue/rplugins",
    author = "xingyue",
    author_email = "qixingyue@126.com",
    package = find_packages(),
    include_package_data = True
)
