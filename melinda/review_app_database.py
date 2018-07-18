import random

import melinda.database.models
from melinda.app import db


def populate():
    db.create_all()

    for name in [
        "Coding",
        "Design",
        "Testing",
        "Protocols",
        "Programming Languages",
        "External Frameworks/Libraries/Tools",
        "Metaswitch Frameworks/Libraries/Tools",
        "Task/Project Management",
        "Pastoral Support",
        "Career Coaching",
    ]:
        tag = melinda.database.models.Tag(name)
        tag.add()

    for i in range(10):
        user = melinda.database.models.User(
            "user{}".format(i),
            "user{}@email.com".format(i),
            "user{} bio".format(i),
            random.choices(["Coding", "Design", "Testing"], k=2),
            "I can teach you anything!",
        )
        user.add()

    for i in range(5):
        melinda.database.models.create_request(
            "user{}@email.com".format(i),
            [random.choice(["Coding", "Design", "Testing"])],
            "Teach me a random thing.",
        )


def clear():
    db.drop_all()


if __name__ == "__main__":
    # This is run as part of the heroku pipelines for staging apps.
    # The live app doesn't run this - it uses the environment DATABASE_URL to connect
    # to the postgres service provided by heroku.
    populate()
