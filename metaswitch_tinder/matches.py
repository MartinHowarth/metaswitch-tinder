"""Module to handle generating matches and handling match requests from mentors and mentees."""

import itertools

from collections import defaultdict
from typing import Dict, List

import metaswitch_tinder.database.models
from metaswitch_tinder import database, tinder_email
from metaswitch_tinder.components.session import is_logged_in, current_username, on_mentee_tab, get_current_user
from metaswitch_tinder.database import get_request_by_id, get_user, list_all_users, User, Request


class Match:
    def __init__(self, other_user: str, their_tags: List[str], bio: str, your_tags: List[str], request_id: str) -> None:
        self.other_user = other_user
        self.their_tags = their_tags
        self.bio = bio
        self.your_tags = your_tags
        self.request_id = request_id

    def __repr__(self):
        return "<Match({self.other_user}, {self.their_tags}, {self.bio}, {self.your_tags}, {self.request_id})".format(
            self=self)


def tag_to_mentor_mapping(mentors: List[User]) -> Dict[str, List[User]]:
    tag_map = defaultdict(list)  # type: Dict[str, List[User]]
    for mentor in mentors:
        for tag in mentor.tags:
            tag_map[tag].append(mentor)
    return tag_map


def tag_to_request_mapping(mentees: List[User]) -> Dict[str, List[Request]]:
    tag_map = defaultdict(list)  # type: Dict[str, List[Request]]
    for mentee in mentees:
        for request in mentee.get_requests():
            for tag in request.tags:
                tag_map[tag].append(request)
    return tag_map


def matches_for_mentee(mentor_tag_map: Dict[str, List[User]], mentee: User) -> List[Match]:
    matches = []
    for request in mentee.get_requests():
        possible_mentors = list(itertools.chain(*[mentor_tag_map[tag] for tag in request.tags]))
        if possible_mentors:
            matches.extend([Match(mentor.name, mentor.tags, mentor.bio, request.tags, request.id)
                            for mentor in possible_mentors])
    return matches


def matches_for_mentor(request_tag_map, mentor: User):
    user = metaswitch_tinder.database.models.get_user(current_username())
    matches = []  # type: List[Match]
    print(user.mentor_matches)
    if user.mentor_matches == '':
        return matches
    for match in user.mentor_matches.split(','):
        username, request_id = match.split(':')
        mentee = metaswitch_tinder.database.models.get_user(username)
        request = metaswitch_tinder.database.models.get_request_by_id(request_id)
        matches.extend([Match(mentee.name, request.tags, mentee.bio, [], request_id)])
    return matches


def generate_matches() -> List[Match]:
    all_users = list_all_users()
    request_tag_map = tag_to_request_mapping(all_users)
    mentor_tag_map = tag_to_mentor_mapping(all_users)

    if not is_logged_in():
        return []

    if on_mentee_tab():
        matches = matches_for_mentee(mentor_tag_map, get_current_user())
    else:
        matches = matches_for_mentor(request_tag_map, get_current_user())

    unique_users = list(set([match.other_user for match in matches]))

    unique_matches = []
    for match in matches:
        if match.other_user in unique_users:
            unique_users.remove(match.other_user)
            unique_matches.append(match)
    return unique_matches


def handle_mentee_reject_match(matched_user: str, request_id: str):
    print("mentee rejected match:", matched_user, request_id)
    mentor = get_user(matched_user)
    request = get_request_by_id(request_id)
    request.handle_mentee_reject_mentor(mentor)


def handle_mentee_accept_match(matched_user: str, matched_tags: List[str], request_id: str):
    print("mentee accepted match:", matched_user, request_id)
    mentor = get_user(matched_user)
    request = get_request_by_id(request_id)
    request.handle_mentee_accept_mentor(mentor)


def handle_mentor_reject_match(matched_user: str, request_id: str):
    print("mentor rejected match:", matched_user, request_id)
    request = get_request_by_id(request_id)
    request.handle_mentee_reject_mentor(get_current_user())


def handle_mentor_accept_match(matched_user: str, matched_tags: List[str], request_id: str):
    print("mentor accepted match:", matched_user, request_id)
    mentor = get_current_user()
    mentee = get_user(matched_user)
    request = get_request_by_id(request_id)
    request.handle_mentor_accept_mentee(mentor)

    email_text = "You've matched on " + (','.join(matched_tags))
    email_text += '\n\n'
    email_text += request.comment

    tinder_email.send_match_email([mentor.email, mentee.email], email_text)
