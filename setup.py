"""
PyMail Utils
-------------

Use this module in order to manage easly emails
"""
from setuptools import setup


setup(
    name='pymailutils',
    version='0.1',
    url='https://github.com/matteogaito/pymailutils',
    license='LICENSE',
    author='Matteo Gaito',
    author_email='matteo@gaito.net',
    description='Module for email interaction with python',
    long_description=__doc__,
    py_modules=['pymailutils'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
