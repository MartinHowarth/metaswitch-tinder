import time

from random import randint
from sqlalchemy_utils import ScalarListType
from typing import List, Optional, Union

from metaswitch_tinder.app import db


class Request(db.Model):
    """
    id - Randomly generated "unique" ID of request
    maker - Name of user who made the request (str)
    tags - Comma separated list of tags
    comment - Comment about request (str)
    """
    id = db.Column(db.String, primary_key=True)
    _maker = db.Column(db.String(80))  # Also the mentee, by definition.
    mentor = db.Column(db.String(80))  # This is the (singular) mentor who has been matched with.
    comment = db.Column(db.String(2000))
    tags = db.Column(ScalarListType())  # type: List[str]
    _possible_mentors = db.Column(ScalarListType())  # type: List[str]
    _rejected_mentors = db.Column(ScalarListType())  # type: List[str]
    _accepted_mentors = db.Column(ScalarListType())  # type: List[str]
    _rejected_mentees = db.Column(ScalarListType())  # type: List[str]

    def __init__(self, maker: str, tags: List[str], comment: str=None):
        self.id = str(time.time()) + str(randint(1, 100))
        self._maker = maker
        self.tags = tags
        self.comment = comment or ''
        self._accepted_mentors = []
        self._possible_mentors = []
        self._rejected_mentors = []
        self.mentor = ''

    def __repr__(self):
        return "Request<{self.id}>(maker={self.maker}, tags={self.tags}, comment={self.comment})".format(self=self)

    def add(self):
        db.session.add(self)

        # Register this request with the user.
        user = self.get_maker()
        user.requests += [self]

        # Now go and work out which mentors are possible matches
        self.populate_initial_possible_mentors()

        self.commit()

    def commit(self):
        db.session.commit()

    @property
    def maker(self) -> str:
        return self._maker

    @maker.setter
    def maker(self, value: Union[str, 'User']):
        if isinstance(value, User):
            self.maker = value.name
        else:
            self.maker = value

    def get_maker(self) -> 'User':
        return get_user(self._maker)

    @property
    def accepted_mentors(self) -> List[str]:
        return self._accepted_mentors

    @accepted_mentors.setter
    def accepted_mentors(self, value: Union[List['User'], List[str]]):
        mentors = []
        for mentor in value:
            if isinstance(mentor, User):
                mentors.append(mentor.name)
            else:
                mentors.append(mentor)

        self._accepted_mentors = list(set(mentors))
        self.commit()

    def get_accepted_mentors(self) -> List['User']:
        return get_users(self.accepted_mentors)

    @property
    def possible_mentors(self) -> List[str]:
        return self._possible_mentors

    @possible_mentors.setter
    def possible_mentors(self, value: Union[List['User'], List[str]]):
        mentors = []
        for mentor in value:
            if isinstance(mentor, User):
                mentors.append(mentor.name)
            else:
                mentors.append(mentor)

        self._possible_mentors = list(set(mentors))
        self.commit()

    def get_possible_mentors(self) -> List['User']:
        return get_users(self.possible_mentors)

    def remove_possible_mentor(self, mentor: Union['User', str]):
        if isinstance(mentor, User):
            name = mentor.name
        else:
            name = mentor

        if name in self.possible_mentors:
            mentors = self.possible_mentors.copy()
            mentors.remove(name)
            self.possible_mentors = mentors
        self.commit()

    @property
    def rejected_mentors(self) -> List[str]:
        return self._rejected_mentors

    @rejected_mentors.setter
    def rejected_mentors(self, value: Union[List['User'], List[str]]):
        mentors = []
        for mentor in value:
            if isinstance(mentor, User):
                mentors.append(mentor.name)
            else:
                mentors.append(mentor)

        self._rejected_mentees = list(set(mentors))
        self.commit()

    def get_rejected_mentors(self) -> List['User']:
        return get_users(self.rejected_mentors)

    def populate_initial_possible_mentors(self):
        all_users = list_all_users()

        possible_mentors = []  # type: List['User']
        for user in all_users:
            if user.could_mentor_for_request(self):
                # Record this user as a possible mentor for this request
                possible_mentors.append(user)

                # And mark that mentor as involved in this request
                user.requests += [self]

        self.possible_mentors = possible_mentors
        self.commit()

    def handle_mentee_accept_mentor(self, mentor: 'User'):
        """Called when a mentee accepts a mentor. A mentee can accept multiple mentors."""
        self.accepted_mentors += [mentor]

    def handle_mentee_reject_mentor(self, mentor: 'User'):
        """Called when a mentee rejects a mentor. A mentee can reject multiple mentors."""
        self.rejected_mentors += [mentor]

    def handle_mentor_accept_mentee(self, mentor: 'User'):
        """Called when a mentor accepts a mentee. This can only be called once."""
        self.mentor = mentor.name
        self.possible_mentors = []
        self.accepted_mentors = []
        self.rejected_mentors = []

        self.commit()

    def handle_mentor_reject_mentee(self, mentor: 'User'):
        """Called when a mentor rejects a mentee."""
        self.rejected_mentors += [mentor]


class User(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120), unique=True)
    bio = db.Column(db.String(2000))
    mentoring_details = db.Column(db.String(2000))
    mentor_matches = db.Column(db.String(2000))
    _mentors = db.Column(ScalarListType())  # type: List[str]
    _mentees = db.Column(ScalarListType())  # type: List[str]

    # Requests that this user is involved with. Both as a mentor and as a mentee.
    _requests = db.Column(ScalarListType())  # type: List[str]
    _tags = db.Column(ScalarListType())  # type: List[str]

    def __init__(self, name: str, email: str, bio: str=None, tags: List[str]=None, mentoring_details: str=None):
        self.name = name
        self.email = email
        self.bio = bio or ''
        self.mentoring_details = mentoring_details or ''
        self.mentor_matches = ""
        self._tags = tags or []

        self._mentees = []
        self._mentors = []
        self._requests = []

    def __repr__(self):
        return (
            "User(name={self.name}, email={self.email}, bio={self.bio}, tags={self.tags})".format(self=self))

    def add(self):
        db.session.add(self)

        self.populate_all_possible_requests_to_mentor()

        self.commit()

    def commit(self):
        db.session.commit()

    @property
    def tags(self) -> List[str]:
        return self._tags

    def set_tags(self, tags: List[str]):
        self._tags = list(set(tags))
        self.commit()

        # Mentoring skills have changed, update possible requests to mentor.
        self.populate_all_possible_requests_to_mentor()

    @property
    def mentees(self) -> List[str]:
        return self._mentees

    @mentees.setter
    def mentees(self, value: Union[List['User'], List[str]]):
        mentees = []
        for mentee in value:
            if isinstance(mentee, User):
                mentees.append(mentee.name)
            else:
                mentees.append(mentee)

        self._mentees = list(set(mentees))
        self.commit()

    def get_mentees(self) -> List['User']:
        return get_users(self.mentees)

    @property
    def mentors(self) -> List[str]:
        return self._mentors

    @mentors.setter
    def mentors(self, value: Union[List['User'], List[str]]):
        mentors = []
        for mentor in value:
            if isinstance(mentor, User):
                mentors.append(mentor.name)
            else:
                mentors.append(mentor)

        self._mentors = list(set(mentors))
        self.commit()

    def get_mentors(self) -> List['User']:
        return get_users(self.mentors)

    @property
    def requests(self) -> List[str]:
        return self._requests

    @requests.setter
    def requests(self, value: Union[List['Request'], List[str]]):
        reqs = []
        for request in value:
            if isinstance(request, Request):
                reqs.append(request.id)
            else:
                reqs.append(request)

        self._requests = list(set(reqs))
        self.commit()

    def get_requests(self) -> List['User']:
        return get_requests_by_ids(self.requests)

    def get_requests_as_mentee(self):
        # Filter to only the requests made by this user.
        return [req for req in self.get_requests() if req.maker == self.name]

    def get_requests_as_mentor(self):
        # Filter to only the requests that this user didn't make.
        # That must be only the ones they are applicable to mentor for.
        requests = [req for req in self.get_requests() if req.maker != self.name]

        # Filter out all the requests this mentor has rejected already
        requests = [req for req in requests if self.name not in req.rejected_mentors]
        return requests

    def populate_all_possible_requests_to_mentor(self):
        requests = list_all_requests()

        matching_requests = []
        for request in requests:
            if self.could_mentor_for_request(request):
                # Mark this user as a possible match for the request
                request.possible_mentors += [self]

                # Mark this user as involved as well.
                matching_requests.append(request)
            else:
                request.remove_possible_mentor(self)

        self.requests = list(set(matching_requests))
        self.commit()

    def add_mentor_match(self, match, request_id):
        if self.mentor_matches == '':
            self.mentor_matches = match + ":" + request_id
        else:
            self.mentor_matches += ',' + match + ":" + request_id
        self.commit()

    def could_mentor_for_request(self, request: Request) -> bool:
        """Returns True if this user could be the mentor for a request. Otherwise False."""
        return any((tag in self.tags for tag in request.tags)) and request.maker != self.name


def list_all_requests() -> List[Request]:
    return Request.query.all()


def get_request_by_id(request_id: str) -> Optional[Request]:
    return Request.query.filter_by(id=request_id).first()


def get_requests_by_ids(request_ids: List[str]) -> List[Request]:
    return Request.query.filter(Request.id.in_(request_ids)).all()


def list_all_users() -> List[User]:
    return User.query.all()


def get_user(user_name: Optional[str]) -> Optional[User]:
    return User.query.filter_by(name=user_name).first()


def get_users(names: List[str]) -> List[User]:
    return User.query.filter(User.id.in_(names)).all()


def handle_signup_submit(username: str, email: str, biography: str=None, categories: List[str]=None, details: str=None):
    print("Signup submitted:", username, email, biography)
    new_user = User(username, email, biography, categories, details)
    new_user.add()


def handle_signin_submit(username: str):
    print("signin submitted:", username)
    all_users = list_all_users()
    all_usernames = [user.name for user in all_users]
    print("all users:", all_usernames)
    if username not in all_usernames:
        raise ValueError("User not found.")
