import dash_html_components as html
import itertools
import logging
import random

from collections import namedtuple
from dash.dependencies import Output, State, Event
from typing import List

from metaswitch_tinder import matches
from metaswitch_tinder.database import get_request_by_id, get_user, User
from metaswitch_tinder.app import app, config
from metaswitch_tinder.components.grid import create_magic_three_row
from metaswitch_tinder.components.session import is_logged_in, on_mentee_tab, get_current_user

log = logging.getLogger(__name__)


Match = namedtuple("Match", ['mentee', 'mentor', 'request'])


def children_no_matches():
    return [
            html.Br(),
            html.Img(src=random.choice(config.sad_ducks),
                     className="rounded-circle", width=200, height=200, id='no-match'),
            html.Br(),
            html.Br(),
            html.P("Aw shucks! You're out of matches!", className="lead"),
            html.P("Refresh the tab to see your skipped matches.", className="lead"),
            html.Div(None, id='current-other-user', hidden=True),
            html.Div(0, id='accept-match', hidden=True),
            html.Div(0, id='reject-match', hidden=True),
            html.Div(None, id='completed-users', hidden=True),
            html.Div(None, id='matched-tags', hidden=True),
            html.Div("", id='matched-request-id', hidden=True),
        ]


def children_for_match(match: Match, skipped_requests: List[str]):
    if on_mentee_tab():
        other_user_name = match.mentor.name
        table_rows = [
            html.Tr([
                html.Td("Name"),
                html.Td(match.mentor.name)
            ], className="table-success"),
            html.Tr([
                html.Td("Mentor skills"),
                html.Td(', '.join(match.mentor.tags))
            ], className="table-success"),
            html.Tr([
                html.Td("Mentor bio"),
                html.Td(match.mentor.bio)
            ], className="table-success"),
        ]
    else:
        other_user_name = match.mentee.name
        table_rows = [
            html.Tr([
                html.Td("Name"),
                html.Td(match.mentee.name)
            ], className="table-success"),
            html.Tr([
                html.Td("Requested skills"),
                html.Td(', '.join(match.request.tags))
            ], className="table-success"),
            html.Tr([
                html.Td("Comment"),
                html.Td(match.request.comment)
            ], className="table-success"),
        ]

    return [
            html.Br(),
            create_magic_three_row([
                html.Button(html.H1("✘"), id='reject-match', className="btn btn-lg btn-secondary"),
                html.Img(src=config.default_user_image,
                         className="rounded-circle", height="100%",
                         id='match-img', draggable='true'),
                html.Button(html.H1("✔"), id='accept-match', className="btn btn-lg btn-primary"),
            ]),
            html.Br(),
            html.Br(),
            html.Table([
                *table_rows
               ], className="table table-condensed"),
            html.Button(html.H1("Skip"), id='skip-match', className="btn btn-lg btn-info"),
            html.Div(other_user_name, id='current-other-user', hidden=True),
            html.Div(skipped_requests, id='skipped-requests', hidden=True),
            html.Div(match.request.id, id='matched-request-id', hidden=True),
        ]


def get_matches_children(skipped_requests: List[str]=list()):
    log.debug("Skipped requests are: %s", skipped_requests)
    current_matches = get_matches_for_current_user_role(skipped_requests)

    if not current_matches:
        children = children_no_matches()
    else:
        match = random.choice(current_matches)
        children = children_for_match(match, skipped_requests)
    return children


def get_matches_for_mentor(mentor: User, skipped_matches: List[str]=list()) -> List[Match]:
    requests = mentor.get_requests_as_mentor()

    _matches = []
    for request in requests:
        # Don't show skipped matches
        # For mentors, skipped_matches is a list of mentee request IDs
        if request.id in skipped_matches:
            continue

        # Don't show matches where this mentor hasn't been accepted by the mentee yet.
        if mentor.name not in request.accepted_mentors:
            continue

        _matches.append(Match(request.get_maker(), mentor, request))
    return _matches


def get_matches_for_mentee(mentee: User, skipped_matches: List[str]=list()) -> List[Match]:
    requests = mentee.get_requests_as_mentee()

    _matches = []
    for request in requests:
        for mentor_name in request.possible_mentors:
            # Don't show skipped matches.
            # For mentees, skipped_matches is a list of mentor names.
            if mentor_name in skipped_matches:
                continue

            # Don't show mentors who have previously been rejected or accepted.
            if mentor_name in itertools.chain(request.rejected_mentors, request.accepted_mentors):
                continue

            _matches.append(Match(mentee, get_user(mentor_name), request))
    return _matches


def get_matches_for_current_user_role(skipped_matches: List[str]) -> List[Match]:
    if on_mentee_tab():
        current_matches = get_matches_for_mentee(get_current_user(), skipped_matches)
    else:
        current_matches = get_matches_for_mentor(get_current_user(), skipped_matches)
    return current_matches


def layout():
    if not is_logged_in():
        return html.Div([html.Br(),
                         html.H1("You must be logged in to do this")])

    return html.Div(
        children=get_matches_children(),
        className="container text-center",
        id="match-div"
    )


def handle_submit(match_request_id: str, other_user_name: str, accepted: bool):
    request = get_request_by_id(match_request_id)
    other_user = get_user(other_user_name)

    if other_user is None:
        raise AssertionError("Could not get other user by name: %s" % other_user_name)

    if request is None:
        raise AssertionError("Could not get request by id: %s" % match_request_id)

    if accepted:
        if on_mentee_tab():
            matches.handle_mentee_accept_match(other_user, request)
        else:
            matches.handle_mentor_accept_match(other_user, request)
    else:
        if on_mentee_tab():
            matches.handle_mentee_reject_match(other_user, request)
        else:
            matches.handle_mentor_reject_match(other_user, request)


def handle_skipped(user_name: str, request_id: str, skipped_matches: List[str]) -> List[str]:
    if on_mentee_tab():
        # For mentees, skipped_matches is a list of mentor names.
        skipped_matches.append(user_name)
    else:
        # For mentors, skipped_matches is a list of mentee request IDs
        skipped_matches.append(request_id)
    return skipped_matches


@app.callback(
    Output('match-div', 'children'),
    [],
    [
        State('current-other-user', 'children'),
        State('accept-match', 'n_clicks'),
        State('reject-match', 'n_clicks'),
        State('skip-match', 'n_clicks'),
        State('skipped-requests', 'children'),
        State('matched-request-id', 'children')
    ],
    [
        Event('accept-match', 'click'),
        Event('reject-match', 'click'),
        Event('skip-match', 'click'),
    ]
)
def submit_mentee_information(other_user, n_accept_clicked, n_reject_clicked, n_skip_clicked,
                              skipped_requests, match_request_id):
    accepted = True if n_accept_clicked else False
    skipped = True if n_skip_clicked else False
    if skipped:
        skipped_requests = handle_skipped(other_user, match_request_id, skipped_requests)
    else:
        handle_submit(match_request_id, other_user, accepted)
    return get_matches_children(skipped_requests)
