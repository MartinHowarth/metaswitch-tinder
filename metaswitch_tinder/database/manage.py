import time

from enum import Enum
from random import randint

from metaswitch_tinder.global_config import DATABASE as db
from random import randint
import time


class User(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120), unique=True)
    bio = db.Column(db.String(2000))
    tags = db.Column(db.String(2000))
    requests = db.Column(db.String(2000))

    def __init__(self, name, email, bio, tags):
        if isinstance(tags, list):
            tags = ','.join(tags)
        self.name = name
        self.email = email
        self.bio = bio
        self.tags = tags
        self.requests = ""
        self.mentor_matches = []

    def __repr__(self):
        return """
        Name - %s
          Email - %s      
          Bio - %s    
          Tags - %s
          Requests - %s
        """ % (self.name, self.email, self.bio, self.tags, self.requests)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return


class Request(db.Model):
    """
    id - Randomly generated "unique" ID of request
    maker - Name of user who made the request (str)
    tags - Comma separated list of tags
    comment - Comment about request (str)
    state - The state of the request, should be
            * unmatched (no match found yet)
            * pending (email sent to potential match)
            * matched (a match has been accepted)
            * rejected (a match has been rejected)
    """
    id = db.Column(db.String, primary_key=True)
    maker = db.Column(db.String(80))
    tags = db.Column(db.String(2000))
    comment = db.Column(db.String(2000))
    state = db.Column(db.String(80))

    class State(Enum):
        UNMATCHED = 'unmatched'
        PENDING = 'pending'
        MATCHED = 'matched'
        REJECTED = 'rejected'

    def __init__(self, maker, tags, comment, state):
        self.id = str(time.time()) + str(randint(1, 100))
        self.maker = maker
        self.tags = tags
        self.comment = comment
        self.state = state

        if isinstance(self.tags, list):
            self.tags = ",".join(self.tags)

    def __repr__(self):
        return """
        ID - %s
        Maker - %s
        Tags - %s
        State - %s
        Comment - %s
        """ % (self.id, self.maker, self.tags, self.state, self.comment)

    def add(self):
        db.session.add(self)

        user = get_user(self.maker)
        user.requests += self.id + ","

        db.session.commit()
        return


def list_whole_table(table):
    return table.query.all()

def list_all_users():
    return User.query.all()


def get_user(match_name):
    return User.query.filter_by(name=match_name).first()


def get_request_by_user(match_name):
    # Return list of all Requests made by "match_name"
    return Request.query.filter_by(maker=match_name).all()


def purge_table(table):
    # Delete all rows in specified table
    table.query.delete()
    db.session.commit()
    return


def delete_table(table):
    # Delete specified table
    table.__table__.drop(db.session.bind)
    db.session.commit()
    return

#db.create_all()
