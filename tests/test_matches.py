from typing import List

from metaswitch_tinder.database import User, get_user, Request, get_request_by_id
from metaswitch_tinder.app import db


class TestMatches:
    def setup_method(self, method):
        db.create_all()

    def teardown_method(self, method):
        db.drop_all()

    def create_user(self, name: str, tags: List[str]=None) -> User:
        user = User(name, '{}@email.com'.format(name), tags=tags)
        print(name, user)
        user.add()
        return user

    def create_request(self, user: User, tags: List[str]) -> Request:
        request = Request(user.name, tags)
        request.add()
        return request

    def delete_user(self, name: str):
        user = get_user(name)
        # TODO

    def test_basic_user_creation(self):
        user = self.create_user('fred', tags=[])
        assert user.name == 'fred'

    def test_user_tags(self):
        # Test initial setting of tags
        tags = ['tag1', 'tag2', 'tag3']
        user = self.create_user('fred', tags=tags)
        assert user.tags == tags

        # Test setting tags after initial setting
        tags2 = tags[:-1]
        user.tags = tags2
        assert user.tags == tags2

    def test_request_creation(self):
        user = self.create_user('fred')
        tags = ['tag1', 'tag2', 'tag3']
        request = self.create_request(user, tags)
        assert request.id in user.requests

    def test_populate_initial_possible_mentors(self):
        """
        This test covers the initial creation of a request, and ensuring that mentors get matched to it correctly.
        """
        request_tags = ['tag1']
        request2_tags = ['tag2']
        mentor1_tags = ['tag1']
        mentor2_tags = ['tag1', 'tag2']

        mentee = self.create_user('mentee')

        # Make the mentors first.
        mentor1 = self.create_user('mentor1', tags=mentor1_tags)
        mentor2 = self.create_user('mentor2', tags=mentor2_tags)

        # Then make the requests.
        # Request 1 should match both mentors
        request1 = self.create_request(mentee, request_tags)

        assert mentor1.name in request1.possible_mentors
        assert mentor2.name in request1.possible_mentors
        assert request1.id in mentor1.requests
        assert request1.id in mentor2.requests

        # Request 2 should only match one mentor
        request2 = self.create_request(mentee, request2_tags)

        assert mentor1.name not in request2.possible_mentors
        assert mentor2.name in request2.possible_mentors
        assert request2.id not in mentor1.requests
        assert request2.id in mentor2.requests

    def test_populate_all_possible_requests_to_mentor(self):
        """
        This test covers creating a new user, and ensuring that they get matches to
        all existing requests they could mentor.
        """
        request1_tags = ['tag1']
        request2_tags = ['tag2']
        mentor1_tags = ['tag1']
        mentor2_tags = ['tag1', 'tag2']

        mentee = self.create_user('mentee')

        # Make the requests first.
        request1 = self.create_request(mentee, request1_tags)
        request2 = self.create_request(mentee, request2_tags)

        # Then make the mentors.
        # Mentor 1 should only match request 1.
        mentor1 = self.create_user('mentor1', tags=mentor1_tags)

        assert request1.id in mentor1.requests
        assert request2.id not in mentor1.requests
        assert mentor1.name in request1.possible_mentors
        assert mentor1.name not in request2.possible_mentors

        # Mentor 2 should match both requests.
        mentor2 = self.create_user('mentor2', tags=mentor2_tags)

        assert request1.id in mentor2.requests
        assert request2.id in mentor2.requests
        assert mentor2.name in request1.possible_mentors
        assert mentor2.name in request2.possible_mentors
