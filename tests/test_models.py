from typing import List

from metaswitch_tinder.app import db
from metaswitch_tinder.database import User, Request, list_all_users, list_all_requests


class TestModels:
    def setup_method(self, method):
        db.create_all()

    def teardown_method(self, method):
        db.drop_all()

    def create_user(self, name: str, tags: List[str]=None) -> User:
        user = User(name, '{}@email.com'.format(name), tags=tags)
        user.add()
        return user

    def create_request(self, user: User, tags: List[str]) -> Request:
        request = Request(user.name, tags)
        request.add()
        return request

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
        user.set_tags(tags2)
        assert len(user.tags) == len(tags2)
        assert set(user.tags) == set(tags2)

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

    def test_match_requests_when_mentor_updates_tags(self):
        request1_tags = ['tag1']
        request2_tags = ['tag2']
        mentor_tags = ['tag1']

        mentee = self.create_user('mentee')

        # Make the requests first.
        request1 = self.create_request(mentee, request1_tags)
        request2 = self.create_request(mentee, request2_tags)

        # Mentor should only match request 1 initially
        mentor = self.create_user('mentor', tags=mentor_tags)

        assert request1.id in mentor.requests
        assert request2.id not in mentor.requests
        assert mentor.name in request1.possible_mentors
        assert mentor.name not in request2.possible_mentors

        # Setting these tags should match both requests
        mentor.set_tags(request1_tags + request2_tags)

        assert request1.id in mentor.requests
        assert request2.id in mentor.requests
        assert mentor.name in request1.possible_mentors
        assert mentor.name in request2.possible_mentors

        # Removing all tags should match no requests
        mentor.set_tags([])

        assert request1.id not in mentor.requests
        assert request2.id not in mentor.requests
        assert mentor.name not in request1.possible_mentors
        assert mentor.name not in request2.possible_mentors

    def test_get_requests_as_mentee(self):
        request1_tags = ['tag1']
        request2_tags = ['tag2']
        mentor_tags = ['tag1', 'tag2']

        mentee = self.create_user('mentee', tags=mentor_tags)

        req_ids = [req.id for req in mentee.get_requests_as_mentee()]
        assert len(req_ids) == 0

        request1 = self.create_request(mentee, request1_tags)
        request2 = self.create_request(mentee, request2_tags)

        self.create_user('mentor', tags=mentor_tags)

        req_ids = [req.id for req in mentee.get_requests_as_mentee()]
        assert len(req_ids) == 2
        assert request1.id in req_ids
        assert request2.id in req_ids

    def test_get_requests_as_mentor(self):
        request1_tags = ['tag1']
        request2_tags = ['tag2']
        mentor_tags = ['tag1', 'tag2']

        mentee = self.create_user('mentee', tags=mentor_tags)

        req_ids = [req.id for req in mentee.get_requests_as_mentor()]
        assert len(req_ids) == 0

        request1 = self.create_request(mentee, request1_tags)
        request2 = self.create_request(mentee, request2_tags)

        mentor = self.create_user('mentor', tags=mentor_tags)

        req_ids = [req.id for req in mentor.get_requests_as_mentor()]
        assert len(req_ids) == 2
        assert request1.id in req_ids
        assert request2.id in req_ids

    def test_delete_user(self):
        # Create a matching pair
        mentee = self.create_user('user0', tags=[])
        mentor = self.create_user('user1', tags=['tag1'])

        request1 = self.create_request(mentee, ['tag1'])
        request2 = self.create_request(mentee, ['tag1'])
        request3 = self.create_request(mentor, ['tag2'])

        request1.handle_mentee_accept_mentor(mentor)
        request2.handle_mentee_accept_mentor(mentor)
        request2.handle_mentor_accept_mentee(mentor)

        # Record some info so we can compare to it after deletion.
        mentee_requests = [request1.id, request2.id]

        # Now delete the mentee
        mentee.delete()

        # Ensure that the mentee isn't in the database of users
        assert mentee.name not in [user.name for user in list_all_users()]

        # Ensure that the mentee has been purged from all requests
        assert mentee.name not in [req.all_involved_users for req in list_all_requests()]

        # Ensure that the requests made by the mentee have been deleted as well
        for req in mentee_requests:
            assert req not in [_req.id for _req in list_all_requests()]

        # Ensure that the mentor has no reference to the deleted requests
        assert mentor.requests == [request3.id]
        assert mentor.matches == []
