"""
Flask Resto
-------------

RESTful APIs with Flask for lazy people
"""
from setuptools import setup

setup(
    name='flask-resto',
    version='0.1.1',
    url='https://github.com/matthewscholefield/flask-resto',
    license='MIT',
    author='Matthew Scholefield',
    author_email='matthew331199@gmail.com',
    description='RESTful APIs with Flask for lazy people',
    long_description=__doc__,
    packages=['flask_resto'],
    install_requires=[
        'Flask',
        'Werkzeug'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
