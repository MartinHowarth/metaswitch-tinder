# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='metaswitch_tinder',

    version='0.0.1',

    description='Metaswitch Tinder',

    url='https://github.com/MartinHowarth/metaswitch-tinder',

    author='Martin Howarth',
    author_email='howarth.martin@gmail.com',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],

    keywords='',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=[
        'dash',
        'dash-renderer',
        'dash-html-components',
        'dash-core-components==0.13.0-rc4',
        'gunicorn',
        'munch',
        'requests',
        'schematics',
        'alembic',
        'Flask-Migrate',
        'Flask-Script',
        'Flask-SQLAlchemy',
        'psycopg2',
    ],
)
