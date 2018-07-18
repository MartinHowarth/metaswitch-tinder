[![CircleCI](https://circleci.com/gh/MartinHowarth/melinda.svg?style=shield)](https://circleci.com/gh/MartinHowarth/melinda)

# Melinda

Melinda is a match-making service for informal mentoring and pastoral support.

It is built using the [dash](https://plot.ly/products/dash/) framework. The Dash framework provides simple python bindings for creating a React.js based app.

For more information (specifically for contributors/developers), see the [wiki](https://github.com/MartinHowarth/melinda/wiki).

## Quickstart development instructions

On Linux, with live updates when you save changes to the source files:
```
yum install -y python36
python36 setup.py develop
python36 melinda/index.py
```

or, to run the app using gunicorn (as it should be when deployed live):
```
gunicorn -w 4 melinda.index:server
```

## Test Database
Test apps use an in-memory postgres database.

It is auto-populated with the test data is defined in `melinda/populate_test_database.py`.

Note: This in-memory database will not be auto-populated when running with gunicorn.
