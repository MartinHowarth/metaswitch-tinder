[![CircleCI](https://circleci.com/gh/MartinHowarth/metaswitch-tinder.svg?style=shield)](https://circleci.com/gh/MartinHowarth/metaswitch-tinder)

# Metaswitch Tinder

Metaswitch Tinder is a match-making service for informal mentoring and unofficial pastoral support at Metaswitch.

It is built using the [dash](https://plot.ly/products/dash/) framework. The Dash framework provides simple python bindings for creating a React.js based app.

For more information (specifically for contributors/developers), see the [wiki](https://github.com/MartinHowarth/metaswitch-tinder/wiki).

## Quickstart development instructions

You will need a postgres database to test against and set the DATABASE_URL environment variable to be its URI.
If you work out how to do that, please submit an MR to document it in this README.

On Linux, with live updates when you save changes to the source files:
```
yum install -y python36
python36 setup.py develop
python36 metaswitch_tinder/index.py
```

or, to run the app using gunicorn (as it should be when deployed live):
```
gunicorn -w 4 metaswitch_tinder.index:server
```

## Test Database
Test apps use an in-memory postgres database.

It is auto-populated with the test data is defined in `metaswitch_tinder/populate_test_database.py`.

Note: This in-memory database will not be auto-populated when running with gunicorn.
