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
        'Programming Language :: Python :: 3.6',
    ],

    keywords='',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=[
        'alembic',
        'dash==0.21.1',
        'dash-html-components==0.10.1',
        'dash-core-components==0.13.0-rc4',
        'dash-renderer==0.12.1',
        'Flask-Migrate',
        'Flask-Script',
        'Flask-SQLAlchemy',
        'gunicorn',
        'munch',
        'plotly==2.6.0',
        'psycopg2',
        'requests',
        'schematics',
        'sendgrid',
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        'pytest',
    ],
)
