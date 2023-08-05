import io
import os

from setuptools import setup, find_packages

setup(
    name='box-python-sdk',
    version="0.0.1",
    description='Not the Box Python SDK',
    long_description="Please see the 'boxsdk' package for the official Box SDK",
    author='Box',
    author_email='oss@box.com',
    python_requires='>=2.7.0',
    url='https://github.com/box/box-python-sdk',
    install_requires=[],
    packages=find_packages(),
    data_files=[('docs', ['README.rst'])],
    include_package_data=True,
    license='Apache Software License, Version 2.0, http://www.apache.org/licenses/LICENSE-2.0',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
