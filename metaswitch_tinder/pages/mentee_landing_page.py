import dash_core_components as dcc
import dash_html_components as html
import logging

from dash.dependencies import Output, State, Event
from flask import session

import metaswitch_tinder.database.matches

from metaswitch_tinder import database
from metaswitch_tinder.app import app
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '')

sign_in = 'sign_in'
submit_request = 'submit_request'


def layout():
    session['is_mentee'] = True
    if 'username' in session:
        is_signed_in_fields = [
            html.H3("Welcome {}!".format(session['username']),
                    className="text-center"),
            # Must include something with the id `email-NAME`, but hidden in this case
            dcc.Input(value='', type='text', id='email-{}'.format(NAME), style={'display': 'none'}),
            dcc.Input(value='', type='text', id='username-{}'.format(NAME), style={'display': 'none'}),
            html.Br(),
            html.Br(),
            html.H3('New mentoring request', className="text-center"),
        ]
    else:
        is_signed_in_fields = [
            html.H3('Existing Users', className="text-center"),
            dcc.Link(html.Button("Sign in",
                                 id='sign-in-{}'.format(NAME),
                                 className="btn btn-lg btn-primary btn-block"),
                     href=href(__name__, sign_in)),
            html.Br(),
            html.Br(),
            html.H3('New mentoring request', className="text-center"),
            html.Br(),
            create_equal_row([
                html.Label('Name:'),
                dcc.Input(value='', type='text', id='username-{}'.format(NAME)),
            ]),
            html.Br(),
            create_equal_row([
                html.Label('Email:',),
                dcc.Input(value='@metaswitch.com', type='text', id='email-{}'.format(NAME)),
            ]),
        ]

    return html.Div([
        html.H1("Metaswitch Tinder", className="text-center"),
        html.Br(),
        *is_signed_in_fields,
        html.Br(),
        html.Label('Mentoring topic:'),
        html.Br(),
        multi_dropdown_with_tags(database.tags.get_tags(), 'categories-{}'.format(NAME)),
        html.Br(),
        html.Label('Additional topic tags:', className="text-center"),
        html.Br(),
        create_equal_row([dcc.Input(value='', type='text', id='details-{}'.format(NAME))]),
        html.Br(),
        dcc.Link(html.Button("Submit my request!",
                             id='submit-{}'.format(NAME),
                             className="btn btn-lg btn-success btn-block"),
                 href=href(__name__, submit_request)),
    ],
        className="container", id='my-div')


@app.callback(
    Output('my-div'.format(NAME), 'children'),
    [],
    [
        State('username-{}'.format(NAME), 'value'),
        State('email-{}'.format(NAME), 'value'),
        State('categories-{}'.format(NAME), 'value'),
        State('details-{}'.format(NAME), 'value'),
    ],
    [Event('submit-{}'.format(NAME), 'click')]
)
def submit_mentee_information(username, email, categories, details):
    print('mentee submit', session)
    print('submit_mentee_information', username, email, categories, details)
    if 'username' not in session:
        session['username'] = username
        metaswitch_tinder.database.matches.handle_mentee_signup_and_request(username, email, categories, details)
    else:
        # If already signed in, only add the request
        metaswitch_tinder.database.matches.handle_mentee_add_request(session['username'], categories, details)
