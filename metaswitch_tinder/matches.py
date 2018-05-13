"""Module to handle generating matches and handling match requests from mentors and mentees."""

import itertools

from collections import defaultdict
from flask import session
from typing import Dict, List

from metaswitch_tinder import database, tinder_email
from metaswitch_tinder.components.auth import is_logged_in, current_username
from metaswitch_tinder.database.manage import get_request_by_id


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


def tag_to_mentor_mapping(mentors: List[database.manage.User]) -> Dict[str, List[database.manage.User]]:
    tag_map = defaultdict(list)  # type: Dict[str, List[database.manage.User]]
    for mentor in mentors:
        for tag in mentor.get_tags():
            tag_map[tag].append(mentor)
    return tag_map


def tag_to_request_mapping(mentees: List[database.manage.User]) -> Dict[str, List[database.manage.Request]]:
    tag_map = defaultdict(list)  # type: Dict[str, List[database.manage.Request]]
    for mentee in mentees:
        for request in mentee.get_requests():
            for tag in request.get_tags():
                tag_map[tag].append(request)
    return tag_map


def matches_for_mentee(mentor_tag_map: Dict[str, List[database.manage.User]],
                       mentee: database.manage.User) -> List[Match]:
    matches = []
    for request in mentee.get_requests():
        possible_mentors = list(itertools.chain(*[mentor_tag_map[tag] for tag in request.get_tags()]))
        if possible_mentors:
            matches.extend([Match(mentor.name, mentor.get_tags(), mentor.bio, request.get_tags(), request.id)
                            for mentor in possible_mentors])
    return matches


def matches_for_mentor(request_tag_map, mentor: database.manage.User):
    user = database.manage.get_user(current_username())
    matches = []  # type: List[Match]
    print(user.mentor_matches)
    if user.mentor_matches == '':
        return matches
    for match in user.mentor_matches.split(','):
        username, request_id = match.split(':')
        mentee = database.manage.get_user(username)
        request = database.manage.get_request_by_id(request_id)
        matches.extend([Match(mentee.name, request.get_tags(), mentee.bio, [], request_id)])
    return matches


def generate_matches() -> List[Match]:
    all_users = database.manage.list_all_users()
    request_tag_map = tag_to_request_mapping(all_users)
    mentor_tag_map = tag_to_mentor_mapping(all_users)

    if not is_logged_in():
        return []

    if 'is_mentee' in session and session['is_mentee']:
        matches = matches_for_mentee(mentor_tag_map, database.manage.get_user(current_username()))
    else:
        matches = matches_for_mentor(request_tag_map, database.manage.get_user(current_username()))

    unique_users = list(set([match.other_user for match in matches]))

    unique_matches = []
    for match in matches:
        if match.other_user in unique_users:
            unique_users.remove(match.other_user)
            unique_matches.append(match)
    return unique_matches


def handle_mentee_reject_match(matched_user: str, request_id: str):
    print("mentee rejected match:", matched_user, request_id)
    database.matches.handle_mentee_reject_match(request_id)


def handle_mentee_accept_match(matched_user: str, matched_tags: List[str], request_id: str):
    print("mentee accepted match:", matched_user, request_id)
    current_user = database.manage.get_user(current_username())
    other_user = database.manage.get_user(matched_user)
    database.matches.handle_mentee_accept_match(request_id, current_user, other_user)


def handle_mentor_reject_match(matched_user: str, request_id: str):
    print("mentor rejected match:", matched_user, request_id)
    database.matches.handle_mentor_reject_match(request_id)


def handle_mentor_accept_match(matched_user: str, matched_tags: List[str], request_id: str):
    print("mentor accepted match:", matched_user, request_id)
    database.matches.handle_mentor_accept_match(request_id)
    request = get_request_by_id(request_id)
    current_user = database.manage.get_user(current_username())
    other_user = database.manage.get_user(matched_user)

    email_text = "You've matched on " + (','.join(matched_tags))
    email_text += '\n\n'
    email_text += request.comment

    tinder_email.send_match_email([current_user.email, other_user.email], email_text)
