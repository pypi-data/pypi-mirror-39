"""
falcon-jinja
------------
Jinja2 support for Falcon web framework
"""

from setuptools import setup

import falcon_jinja2

setup(
    name='falcon_jinja2',
    version=falcon_jinja2.__version__,
    url='https://github.com/mikeylight/falcon-jinja',
    license=falcon_jinja2.__license__,
    author=falcon_jinja2.__author__,
    author_email='mikeiceman1221@gmail.com',
    description='Jinja2 support for Falcon',
    long_description=__doc__,
    packages=['falcon_jinja2'],
    platforms='any',
    install_requires=[
        'jinja2',
        'falcon'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]

)
