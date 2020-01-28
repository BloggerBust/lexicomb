import os
from setuptools import setup, find_namespace_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="lexicomb",
    version="0.0.1",
    author="Trevor Wilson",
    author_email="trevor.wilson@bloggerbust.ca",
    description=("Lexicomb - a BloggerBust Project"),
    license="Apache License v2.0",
    keywords="BloggerBust projects: lexical analyzer, parser combinator, tag system",
    url="https://bloggerbust.ca",
    # read('README.md'),
    long_description="A simple language where you build your own lexicon",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Software Development",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License"
    ],
    namespace_packages=["bbpyp"],
    packages=find_namespace_packages(include=["bbpyp.*"]),
    python_requires=">=3.5",
    install_requires=[
        "bbpyp==0.0.1"
    ],
    extras_require={
        "dev": [
            "mock==3.0.5",
            "autopep8== 1.3.2"
        ]
    },
    zip_safe=False,  # sorry, no eggs
    test_suite='test'
)
