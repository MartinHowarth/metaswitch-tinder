import random

from metaswitch_tinder.app import db
from metaswitch_tinder.database import manage


def populate():
    db.create_all()

    for i in range(10):
        user = manage.User(
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
        req = manage.Request(
            'user{}'.format(i),
            random.choice(['Coding', 'Design', 'Testing']),
            "Teach me a random thing.",
        )
        req.add()
