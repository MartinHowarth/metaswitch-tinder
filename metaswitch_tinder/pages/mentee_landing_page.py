import dash_core_components as dcc
import dash_html_components as html
import logging

from dash.dependencies import Output, State, Event

import metaswitch_tinder.database.models

from metaswitch_tinder.app import app
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components import session
from metaswitch_tinder.components.grid import create_equal_row

from . import mentee_request


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '_')

sign_in = 'sign_in'


def layout():
    if session.is_logged_in():
        is_signed_in_fields = [
            html.H3("Welcome {}!".format(session.current_username()),
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
        mentee_request.layout(),
    ],
        className="container", id='my-div')


@app.callback(
    Output('my-div'.format(NAME), 'children'),
    [],
    [
        State('username-{}'.format(NAME), 'value'),
        State('email-{}'.format(NAME), 'value'),
    ],
    [Event(mentee_request.submit_button, 'click')]
)
def submit_mentee_information(username, email):
    log.info('signin (as part of initial mentee request): %s - %s', username, email)
    if not session.is_logged_in():
        session.login(username)
        metaswitch_tinder.database.models.handle_signup_submit(username, email)
