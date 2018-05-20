from typing import Generator, List, Optional

from metaswitch_tinder.app import db
from . import Request, get_requests_by_ids, list_all_requests


class User(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    email = db.Column(db.String(120), unique=True)
    bio = db.Column(db.String(2000))
    mentoring_details = db.Column(db.String(2000))
    mentor_matches = db.Column(db.String(2000))
    _mentors = db.Column(db.String(2000))
    _mentees = db.Column(db.String(2000))

    # Requests that this user is involved with. Both as a mentor and as a mentee.
    _requests = db.Column(db.String(2000))
    _tags = db.Column(db.String(2000))

    def __init__(self, name: str, email: str, bio: str=None, tags: List[str]=None, mentoring_details: str=None):
        self.name = name
        self.email = email
        self.bio = bio or ''
        self.mentoring_details = mentoring_details or ''
        self.mentor_matches = ""
        self.tags = tags or []

        self._mentees = ''
        self._mentors = ''
        self._requests = ''

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

        self.populate_all_possible_requests_to_mentor()

        self.commit()

    def commit(self):
        db.session.commit()

    def add_request(self, request: Request):
        # Append directly to avoid loading all other requests from the database
        self._requests += ',' + request.id
        self.commit()

    @property
    def mentees(self) -> Generator[str]:
        return (get_user(name) for name in self._mentees.split(','))

    @mentees.setter
    def mentees(self, value: List['User']):
        self._mentees = ','.join([user.name for user in value])
        self.commit()

    @property
    def mentors(self) -> Generator[str]:
        return (get_user(name) for name in self._mentors.split(','))

    @mentors.setter
    def mentors(self, value: List['User']):
        self._mentors = ','.join([user.name for user in value])
        self.commit()

    @property
    def tags(self) -> List[str]:
        return self._tags.split(',')

    @tags.setter
    def tags(self, value: List[str]):
        self._tags = ','.join(value)
        self.commit()

        # Mentoring skills have changed, update possible requests to mentor.
        self.populate_all_possible_requests_to_mentor()

    @property
    def requests(self) -> List[Request]:
        return get_requests_by_ids(self._requests.split(','))

    @requests.setter
    def requests(self, value: List[Request]):
        self._requests = ','.join([req.id for req in value])
        self.commit()

    def populate_all_possible_requests_to_mentor(self):
        requests = list_all_requests()

        for request in requests:
            if self.is_match_for_request(request):
                # Mark this user as a possible match for the request
                request.possible_mentors.append(self)

                # Mark this user as involved as well.
                self._requests += ',' + request.id
        self.commit()

    def add_mentor_match(self, match, request_id):
        if self.mentor_matches == '':
            self.mentor_matches = match + ":" + request_id
        else:
            self.mentor_matches += ',' + match + ":" + request_id
        self.commit()

    def is_match_for_request(self, request: Request) -> bool:
        """Returns True if this user could be the mentor for a request. Otherwise False."""
        return any((tag in self.tags for tag in request.tags)) and request.maker != self.name


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
