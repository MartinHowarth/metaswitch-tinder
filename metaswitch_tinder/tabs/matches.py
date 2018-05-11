import dash_core_components as dcc
import dash_html_components as html
import random

from dash.dependencies import Input, Output, State, Event
from flask import session

from metaswitch_tinder import global_config, matches, database
from metaswitch_tinder.components.grid import create_magic_three_row


def children_no_matches():
    return [
            html.Br(),
            html.Img(src=random.choice(global_config.Global.CONFIG.sad_ducks),
                     className="rounded-circle", width=200, height=200),
            html.Br(),
            html.Br(),
            html.P("Aw shucks! You're out of matches!", className="lead"),
            html.Br(),
            html.A(html.Button("Return to start", className="btn btn-primary btn-lg btn-block"),
                   href='/mentee-landing-page'),
            html.Br(),
            html.Button("Done", id='done', className="btn btn-primary btn-lg btn-block"),
            html.Div(None, id='current-other-user', style={'display': 'none'}),
            html.Div(0, id='accept-match', style={'display': 'none'}),
            html.Div(0, id='reject-match', style={'display': 'none'}),
            html.Div(None, id='completed-users', style={'display': 'none'}),
            html.Div(None, id='matched-tags', style={'display': 'none'}),
        ]


def children_for_match(match: matches.Match, completed_users):
    return [
            html.Br(),
            create_magic_three_row([
                html.Button("✘", id='reject-match', className="btn btn-lg btn-secondary"),
                html.Img(src=global_config.Global.CONFIG.default_user_image,
                         className="rounded-circle", height="100%",
                         id='match-img', draggable='true'),
                html.Button("✔", id='accept-match', className="btn btn-lg btn-primary"),
            ]),

            html.Br(),
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
            html.Button("Done", id='done', className="btn btn-primary btn-lg btn-block"),
            html.Div(match.other_user, id='current-other-user', style={'display': 'none'}),
            html.Div(completed_users, id='completed-users', style={'display': 'none'}),
            html.Div(list(set(match.their_tags) & set(match.your_tags)), id='matched-tags', style={'display': 'none'})
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


def matches_done():
    return [
        html.Br(),
        html.H4("Thanks, your request has been submitted",
                className="text-center"),
        html.Br(),
        html.A(html.Button("Make another request?", className="btn btn-primary btn-lg btn-block"),
               href='/mentee-landing-page'),
        html.Br(),
        html.A(html.Button("Create account?", className="btn btn-primary btn-lg btn-block"),
               href='/mentee-signup')
    ]


def matches_tab():
    print('matches', session)
    return html.Div(
        children=get_matches_children(),
        className="container text-center",
        id="match-div"
    )


def add_callbacks(app):
    @app.callback(
        Output('match-div', 'children'),
        [],
        [
            State('current-other-user', 'children'),
            State('accept-match', 'n_clicks'),
            State('reject-match', 'n_clicks'),
            State('done', 'n_clicks'),
            State('completed-users', 'children'),
            State('matched-tags', 'children')
        ],
        [
            Event('accept-match', 'click'),
            Event('reject-match', 'click'),
            Event('done', 'click'),
        ]
    )
    def submit_mentee_information(other_user, n_accept_clicked, n_reject_clicked, n_done_clicked, completed_users,
                                  matched_tags):
        if n_done_clicked:
            return matches_done()
        if n_accept_clicked:
            if session['is_mentee']:
                matches.handle_mentee_accept_match(other_user)
            else:
                matches.handle_mentor_accept_match(other_user, matched_tags)
        else:
            if session['is_mentee']:
                matches.handle_mentee_reject_match(other_user)
            else:
                matches.handle_mentor_reject_match(other_user)
        completed_users.append(other_user)
        return get_matches_children(completed_users)
