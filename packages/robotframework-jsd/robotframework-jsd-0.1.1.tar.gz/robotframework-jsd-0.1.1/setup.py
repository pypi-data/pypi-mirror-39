# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join
from setuptools import setup

version_file = join(dirname(abspath(__file__)), 'JsdLibrary', 'version.py')

with open(version_file) as f:
    code = compile(f.read(), version_file, 'exec')
    exec code

setup(
    name='robotframework-jsd',
    version=VERSION,
    description='JSD validator for robotframework',
    author='mangobowl',
    author_email='mangobowl@163.com',
    license='BSD License',
    keywords='robotframework testing test automation json json-schema',
    packages=['JsdLibrary'],
    install_requires=[
        'robotframework<3.0',
        'jsonschema<3.0'
    ],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Testing'
    ],
)
