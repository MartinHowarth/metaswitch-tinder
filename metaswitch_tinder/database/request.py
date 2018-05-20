import time

from random import randint
from typing import Generator, List, Optional

from metaswitch_tinder.app import db
from . import get_user, User, list_all_users, get_users


class Request(db.Model):
    """
    id - Randomly generated "unique" ID of request
    maker - Name of user who made the request (str)
    tags - Comma separated list of tags
    comment - Comment about request (str)
    state - The state of the request, should be
            * unmatched (no match found yet)
            * matched (a match has been accepted)
    """
    id = db.Column(db.String, primary_key=True)
    maker = db.Column(db.String(80))  # Also the mentee, by definition.
    mentor = db.Column(db.String(80))  # This is the (singular) mentor who has been matched with.
    comment = db.Column(db.String(2000))
    _tags = db.Column(db.String(2000))
    _possible_mentors = db.Column(db.String(2000))
    _rejected_mentors = db.Column(db.String(2000))
    _accepted_mentors = db.Column(db.String(2000))
    _rejected_mentees = db.Column(db.String(2000))

    def __init__(self, maker: str, tags: List[str], comment: str=None):
        self.id = str(time.time()) + str(randint(1, 100))
        self.maker = maker
        self.tags = tags
        self.comment = comment or ''
        self._accepted_mentors = ''
        self._possible_mentors = ''
        self._rejected_mentors = ''
        self.mentor = ''

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

        # Register this request with the user.
        user = self.get_maker()
        user.add_request(self)

        # Now go and work out which mentors are possible matches
        self.populate_initial_possible_mentors()

        self.commit()

    def commit(self):
        db.session.commit()

    def get_maker(self) -> User:
        return get_user(self._maker)

    @property
    def tags(self) -> List[str]:
        return self._tags.split(',')

    @tags.setter
    def tags(self, value: List[str]):
        self._tags = ','.join(value)
        self.commit()

    # TODO make this a `get_thing` too get the actual database objects, but a standard property to just get the list.
    @property
    def accepted_mentors(self) -> List[User]:
        return get_users(self._accepted_mentors.split(','))

    @accepted_mentors.setter
    def accepted_mentors(self, value: List[User]):
        self._accepted_mentors = ','.join((user.name for user in value))
        self.commit()

    @property
    def possible_mentors(self) -> List[User]:
        return get_users(self._possible_mentors.split(','))

    @possible_mentors.setter
    def possible_mentors(self, value: List[User]):
        self._possible_mentors = ','.join((user.name for user in value))
        self.commit()

    @property
    def rejected_mentors(self) -> List[User]:
        return get_users(self._rejected_mentors.split(','))

    @rejected_mentors.setter
    def rejected_mentors(self, value: List[User]):
        self._rejected_mentors = ','.join((user.name for user in value))
        self.commit()

    def populate_initial_possible_mentors(self):
        all_users = list_all_users()

        possible_mentors = []  # type: List[User]
        for user in all_users:
            if any((tag in user.tags for tag in self.tags)) and user.name != self.maker:
                # Record this user as a possible mentor for this request
                possible_mentors.append(user)

                # And mark that mentor as involved in this request
                user.requests.append(self)

        self.possible_mentors = possible_mentors
        self.commit()

    def handle_mentee_accept_mentor(self, mentor: User):
        """Called when a mentee accepts a mentor. A mentee can accept multiple mentors."""
        self._accepted_mentors += ',' + mentor.name
        self.commit()

    def handle_mentee_reject_mentor(self, mentor: User):
        """Called when a mentee rejects a mentor. A mentee can reject multiple mentors."""
        self._rejected_mentors += ',' + mentor.name
        self.commit()

    def handle_mentor_accept_mentee(self, mentor: User):
        """Called when a mentor accepts a mentee. This can only be called once."""
        self.mentor = mentor.name
        self._possible_mentors = ''
        self._accepted_mentors = ''
        self._rejected_mentors = ''

        self.commit()

    def handle_mentor_reject_mentee(self, mentor: User):
        """Called when a mentor rejects a mentee."""
        self._rejected_mentors += ',' + mentor.name
        self.commit()


def list_all_requests() -> List[Request]:
    return Request.query.all()


def get_request_by_id(request_id: str) -> Optional[Request]:
    return Request.query.filter_by(id=request_id).first()


def get_requests_by_ids(request_ids: List[str]) -> List[Request]:
    return Request.query.filter(Request.id.in_(request_ids)).all()
