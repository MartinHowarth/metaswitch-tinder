import itertools

from collections import defaultdict
from flask import session
from typing import List

from metaswitch_tinder import database, tinder_email


class Match:
    def __init__(self, other_user, their_tags, bio, your_tags):
        self.other_user = other_user
        self.their_tags = their_tags
        self.bio = bio
        self.your_tags = your_tags


def tag_to_mentor_mapping(mentors: List[database.manage.User]):
    tag_map = defaultdict(list)
    for mentor in mentors:
        for tag in mentor.tags:
            tag_map[tag].append(mentor)
    return tag_map


def tag_to_request_mapping(mentees: List[database.manage.User]):
    tag_map = defaultdict(list)
    for mentee in mentees:
        for request in mentee.requests:
            for tag in request.tags:
                tag_map[tag].append(request)
    return tag_map


def matches_for_mentee(mentor_tag_map, mentee: database.manage.User):
    matches = []
    for request in mentee.requests:
        possible_mentors = list(itertools.chain(*[mentor_tag_map[tag] for tag in request.tags]))
        if possible_mentors:
            matches.extend([Match(mentor.username, mentor.tags, mentor.bio, request.tags) for mentor in possible_mentors])
    return matches


def matches_for_mentor(request_tag_map, mentor: database.manage.User):
    matches = []
    possible_requests = list(itertools.chain(*[request_tag_map[tag] for tag in mentor.tags]))
    if possible_requests:
        matches.extend([Match('hidden', request.tags, request.details, mentor.tags) for request in possible_requests])
    return matches


def generate_matches():
    all_users = database.manage.list_all_users()
    request_tag_map = tag_to_request_mapping(all_users)
    mentor_tag_map = tag_to_mentor_mapping(all_users)

    if 'username' not in session:
        return []

    if 'is_mentee' in session and session['is_mentee']:
        return matches_for_mentee(mentor_tag_map, database.manage.get_user(session['username']))
    return matches_for_mentor(request_tag_map, database.manage.get_user(session['username']))


def handle_mentee_reject_match(matched_user):
    print("mentee rejected match:", matched_user)
    database.matches.handle_mentee_reject_match(matched_user)


def handle_mentee_accept_match(matched_user):
    print("mentee accepted match:", matched_user)
    database.matches.handle_mentee_accept_match(matched_user)
    current_user = database.manage.get_user(session['username'])
    other_user = database.manage.get_user(matched_user)
    tinder_email.send_email([current_user.email, other_user.email], "You've matched on ...")
    # TODO - make the email text better

    # TODO - Add the mentee to the list of matches for the mentor


def handle_mentor_reject_match(matched_user):
    print("mentor rejected match:", matched_user)
    database.matches.handle_mentor_reject_match(matched_user)


def handle_mentor_accept_match(matched_user, matched_tags):
    print("mentor accepted match:", matched_user)
    database.matches.handle_mentor_accept_match(matched_user)
    current_user = database.manage.get_user(session['username'])
    other_user = database.manage.get_user(matched_user)
    tinder_email.send_email([current_user.email, other_user.email], "You've matched on " + (','.join(matched_tags)))
    # TODO - make the email text better
