from setuptools import setup, find_packages


setup(
    name="id",
    version="0.1.0",
    author="Leo Tong",
    author_email="tonglei@qq.com",
    description="xuexi",
    long_description=open("README.rst").read(),
    license="Apache License, Version 2.0",
    url="https://github.com/Sweeterio/id",
    packages=['id'],
    package_data={'id': ['*.py']},
    install_requires=[
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.6"
    ],
    entry_points={

    }
)
