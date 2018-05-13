import dash_core_components as dcc
import dash_html_components as html
import logging
import random

from dash.dependencies import Output, State, Event
from flask import session

from metaswitch_tinder import matches
from metaswitch_tinder.app import app, config
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components.grid import create_magic_three_row


log = logging.getLogger(__name__)


make_a_request = 'make_a_request'


def children_no_matches():
    return [
            html.Br(),
            html.Img(src=random.choice(config.sad_ducks),
                     className="rounded-circle", width=200, height=200, id='no-match'),
            html.Br(),
            html.Br(),
            html.P("Aw shucks! You're out of matches!", className="lead"),
            html.Br(),
            dcc.Link(html.Button("Make a request", className="btn btn-primary btn-lg btn-block"),
                     href=href(__name__, make_a_request)),
            html.Br(),
            html.Div(None, id='current-other-user', style={'display': 'none'}),
            html.Div(0, id='accept-match', style={'display': 'none'}),
            html.Div(0, id='reject-match', style={'display': 'none'}),
            html.Div(None, id='completed-users', style={'display': 'none'}),
            html.Div(None, id='matched-tags', style={'display': 'none'}),
            html.Div("", id='matched-request-id', style={'display': 'none'}),
        ]


def children_for_match(match: matches.Match, completed_users):
    your_tags = match.your_tags
    their_tags = match.their_tags
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
                html.Tr([
                    html.Td("Tags"),
                    html.Td(', '.join(match.their_tags))
                ], className="table-success"),
                html.Tr([
                    html.Td("Bio"),
                    html.Td(match.bio)
                ], className="table-success"),
               ], className="table table-condensed"),
            dcc.Link(html.Button("Find a mentor - Make a request", className="btn btn-primary btn-lg btn-block"),
                     href=href(__name__, make_a_request)),
            html.Div(match.other_user, id='current-other-user', style={'display': 'none'}),
            html.Div(completed_users, id='completed-users', style={'display': 'none'}),
            html.Div(list(set(their_tags) & set(your_tags)), id='matched-tags', style={'display': 'none'}),
            html.Div(match.request_id, id='matched-request-id', style={'display': 'none'}),
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
    print('matches', session)
    if 'username' not in session:
        print('not logged in', session)
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
        if session['is_mentee']:
            matches.handle_mentee_accept_match(other_user, matched_tags, match_request_id)
        else:
            matches.handle_mentor_accept_match(other_user, matched_tags, match_request_id)
    else:
        if session['is_mentee']:
            matches.handle_mentee_reject_match(other_user, match_request_id)
        else:
            matches.handle_mentor_reject_match(other_user, match_request_id)
    completed_users.append(other_user)
    return get_matches_children(completed_users)
