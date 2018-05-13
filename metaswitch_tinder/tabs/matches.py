import dash_html_components as html
import logging
import random

from dash.dependencies import Output, State, Event

from metaswitch_tinder import matches
from metaswitch_tinder.database.manage import get_request_by_id, get_user
from metaswitch_tinder.app import app, config
from metaswitch_tinder.components.grid import create_magic_three_row
from metaswitch_tinder.components.session import is_logged_in, on_mentee_tab


log = logging.getLogger(__name__)


def children_no_matches():
    return [
            html.Br(),
            html.Img(src=random.choice(config.sad_ducks),
                     className="rounded-circle", width=200, height=200, id='no-match'),
            html.Br(),
            html.Br(),
            html.P("Aw shucks! You're out of matches!", className="lead"),
            html.Div(None, id='current-other-user', hidden=True),
            html.Div(0, id='accept-match', hidden=True),
            html.Div(0, id='reject-match', hidden=True),
            html.Div(None, id='completed-users', hidden=True),
            html.Div(None, id='matched-tags', hidden=True),
            html.Div("", id='matched-request-id', hidden=True),
        ]


def children_for_match(match: matches.Match, completed_users):
    your_tags = match.your_tags
    their_tags = match.their_tags

    if on_mentee_tab():
        mentor = get_user(match.other_user)
        table_rows = [
            html.Tr([
                html.Td("Mentor skills"),
                html.Td(', '.join(mentor.get_tags()))
            ], className="table-success"),
            html.Tr([
                html.Td("Mentor bio"),
                html.Td(mentor.bio)
            ], className="table-success"),
        ]
    else:
        request = get_request_by_id(match.request_id)
        table_rows = [
            html.Tr([
                html.Td("Requested skills"),
                html.Td(', '.join(request.get_tags()))
            ], className="table-success"),
            html.Tr([
                html.Td("Comment"),
                html.Td(request.comment)
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
                html.Tr([
                    html.Td("Name"),
                    html.Td(match.other_user)
                ], className="table-success"),
                *table_rows
               ], className="table table-condensed"),
            html.Div(match.other_user, id='current-other-user', hidden=True),
            html.Div(completed_users, id='completed-users', hidden=True),
            html.Div(list(set(their_tags) & set(your_tags)), id='matched-tags', hidden=True),
            html.Div(match.request_id, id='matched-request-id', hidden=True),
        ]


def get_matches_children(completed_users=list()):
    current_matches = matches.generate_matches()
    print(current_matches)
    for user in completed_users:
        for match in current_matches:
            if user == match.other_user:
                current_matches.remove(match)
    if not current_matches:
        children = children_no_matches()
    else:
        match = random.choice(current_matches)
        children = children_for_match(match, completed_users)
    return children


def layout():
    if not is_logged_in():
        return html.Div([html.Br(),
                         html.H1("You must be logged in to do this")])
    return html.Div(
        children=get_matches_children(),
        className="container text-center",
        id="match-div"
    )


@app.callback(
    Output('match-div', 'children'),
    [],
    [
        State('current-other-user', 'children'),
        State('accept-match', 'n_clicks'),
        State('reject-match', 'n_clicks'),
        State('completed-users', 'children'),
        State('matched-tags', 'children'),
        State('matched-request-id', 'children')
    ],
    [
        Event('accept-match', 'click'),
        Event('reject-match', 'click'),
    ]
)
def submit_mentee_information(other_user, n_accept_clicked, n_reject_clicked, completed_users,
                              matched_tags, match_request_id):
    if n_accept_clicked:
        if on_mentee_tab():
            matches.handle_mentee_accept_match(other_user, matched_tags, match_request_id)
        else:
            matches.handle_mentor_accept_match(other_user, matched_tags, match_request_id)
    else:
        if on_mentee_tab():
            matches.handle_mentee_reject_match(other_user, match_request_id)
        else:
            matches.handle_mentor_reject_match(other_user, match_request_id)
    completed_users.append(other_user)
    return get_matches_children(completed_users)
