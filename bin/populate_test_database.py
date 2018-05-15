#! python3
"""
This is run as part of the heroku pipelines for staging apps.

The live app doesn't run this - it uses the environment DATABASE_URL to connect
to the postgres service provided by heroku.
"""

from metaswitch_tinder import populate_test_database

populate_test_database.populate()
