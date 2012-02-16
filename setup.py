from distutils.core import setup
from setuptools import find_packages

from hashed_url import __version__

setup(
    name='django-hashed-url',
    version=__version__,
    description="Package for pre-authorising URLs using a hash parameter",
    author="Adam Charnock",
    author_email="adam@playnice.ly",
    url="https://github.com/continuous/django-hashed-url",
    license="Apache Software License",
    
    install_requires=["django"],
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 2.6",
        "Topic :: Security",
        "Framework :: Django",
    ],
    
    packages=find_packages(),
)