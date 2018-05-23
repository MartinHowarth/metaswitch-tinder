from typing import List, Tuple

from metaswitch_tinder.app import db
from metaswitch_tinder.database import User, Request
from metaswitch_tinder.tabs.matches import get_matches_for_mentee, get_matches_for_mentor


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
        request = Request(user, tags)
        request.add()
        return request

    def create_matching_pair(self) -> Tuple[User, User, Request]:
        user0 = self.create_user('user0', tags=[])
        user1 = self.create_user('user1', tags=['tag1'])

        req1 = self.create_request(user0, ['tag1'])

        return user0, user1, req1

    def test_match_mentee_accept_mentor_accept(self):
        mentee, mentor, req1 = self.create_matching_pair()

        # Ensure that the mentor has no matches
        mentor_matches = get_matches_for_mentor(mentor)
        mentee_matches = get_matches_for_mentee(mentee)
        assert len(mentor_matches) == 0
        assert len(mentee_matches) == 1

        # Accept the match from the mentee
        req1.handle_mentee_accept_mentor(mentor)

        # The mentor should now have a match
        # The mentee should no longer have any matches.
        mentor_matches = get_matches_for_mentor(mentor)
        mentee_matches = get_matches_for_mentee(mentee)
        assert len(mentor_matches) == 1
        assert len(mentee_matches) == 0

        # Accept the match from the mentor
        req1.handle_mentor_accept_mentee(mentor)

        # Neither user should have any matches now.
        mentor_matches = get_matches_for_mentor(mentor)
        mentee_matches = get_matches_for_mentee(mentee)
        assert len(mentor_matches) == 0
        assert len(mentee_matches) == 0

        # Both should have one match.
        assert len(mentee.matches) == 1
        assert len(mentor.matches) == 1

    def test_match_mentee_accept_mentor_reject(self):
        mentee, mentor, req1 = self.create_matching_pair()

        # Ensure that the mentor has no matches
        mentor_matches = get_matches_for_mentor(mentor)
        mentee_matches = get_matches_for_mentee(mentee)
        assert len(mentor_matches) == 0
        assert len(mentee_matches) == 1

        # Accept the match from the mentee
        req1.handle_mentee_accept_mentor(mentor)

        # The mentor should now have a match
        # The mentee should no longer have any matches.
        mentor_matches = get_matches_for_mentor(mentor)
        mentee_matches = get_matches_for_mentee(mentee)
        assert len(mentor_matches) == 1
        assert len(mentee_matches) == 0

        # Reject the match from the mentor
        req1.handle_mentor_reject_mentee(mentor)

        # Neither user should have any matches now.
        mentor_matches = get_matches_for_mentor(mentor)
        mentee_matches = get_matches_for_mentee(mentee)
        assert len(mentor_matches) == 0
        assert len(mentee_matches) == 0

        # Neither should have a match.
        assert len(mentee.matches) == 0
        assert len(mentor.matches) == 0

    def test_match_mentee_reject(self):
        mentee, mentor, req1 = self.create_matching_pair()

        # Ensure that the mentor has no matches
        mentor_matches = get_matches_for_mentor(mentor)
        mentee_matches = get_matches_for_mentee(mentee)
        assert len(mentor_matches) == 0
        assert len(mentee_matches) == 1

        # Reject the match from the mentee
        req1.handle_mentee_reject_mentor(mentor)

        # Neither user should have any matches now.
        mentor_matches = get_matches_for_mentor(mentor)
        mentee_matches = get_matches_for_mentee(mentee)
        assert len(mentor_matches) == 0
        assert len(mentee_matches) == 0

        # Neither should have a match.
        assert len(mentee.matches) == 0
        assert len(mentor.matches) == 0
