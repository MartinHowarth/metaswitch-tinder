import random

import metaswitch_tinder.database.request
import metaswitch_tinder.database.user
from metaswitch_tinder.app import db


def populate():
    db.create_all()

    for i in range(10):
        user = metaswitch_tinder.database.user.User(
            'user{}'.format(i),
            'user{}@email.com'.format(i),
            'user{} bio'.format(i),
            ['Coding',
             'Design',
             'Testing'],
            'I can teach you anything!'
        )
        user.add()

    for i in range(5):
        req = metaswitch_tinder.database.request.Request(
            'user{}'.format(i),
            random.choice(['Coding', 'Design', 'Testing']),
            "Teach me a random thing.",
        )
        req.add()


def clear():
    db.drop_all()


if __name__ == "__main__":
    # This is run as part of the heroku pipelines for staging apps.
    # The live app doesn't run this - it uses the environment DATABASE_URL to connect
    # to the postgres service provided by heroku.
    populate()
