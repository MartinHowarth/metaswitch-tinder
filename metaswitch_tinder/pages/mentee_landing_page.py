import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event
from flask import session

import metaswitch_tinder.database.matches
from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags
from metaswitch_tinder import database


NAME = __name__.replace('.', '')


def mentee_landing_page():
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
            html.A(html.Button("Sign in",
                               id='sign-in-{}'.format(NAME),
                               className="btn btn-lg btn-primary btn-block"),
                   href='/mentee-signin'),
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
        html.A(html.Button("Submit my request!",
                           id='submit-{}'.format(NAME),
                           className="btn btn-lg btn-success btn-block"),
               href='/mentee-menu')
    ],
        className="container", id='my-div')


def add_callbacks(app):
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
        session['username'] = username
        print('mentee submit', session)
        metaswitch_tinder.database.matches.handle_mentee_added_request(username, email, categories, details)
        return
