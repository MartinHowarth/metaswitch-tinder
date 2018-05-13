import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Output, State, Event
from flask import session
import logging

from metaswitch_tinder import database
from metaswitch_tinder.app import app
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '')

submit = 'submit'


def layout():
    session['is_mentee'] = False
    return html.Div([
        html.H1("Metaswitch Tinder", className="text-center"),
        html.Br(),
        create_equal_row([
            html.Label('Username:', ),
            dcc.Input(value='', type='text', id='username-{}'.format(NAME)),
        ]),
        html.Br(),
        create_equal_row([
            html.Label('Email:'),
            dcc.Input(value='@metaswitch.com', type='text', id='email-{}'.format(NAME)),
        ]),
        html.Br(),
        create_equal_row([
            html.Label('Location:', ),
            dcc.Input(value='', placeholder='Which office are you in?', type='text', id='location-{}'.format(NAME)),
        ]),
        html.Br(),
        create_equal_row([html.Label('Biography:')]),
        dcc.Textarea(placeholder='Enter a biography', value='Loves ducks',
                     id='biography-{}'.format(NAME), style={'width': '100%'}),
        html.Br(),
        create_equal_row([html.Label('Mentoring topics:')]),
        multi_dropdown_with_tags(database.tags.get_tags(), 'categories-{}'.format(NAME)),
        html.Br(),
        create_equal_row([html.Label('Additional topic tags:')]),
        create_equal_row([
            dcc.Input(placeholder='e.g. \"python\", \"object-oriented design\", \"session-based testing\"',
                      value='', type='text', id='details-{}'.format(NAME))
        ]),
        html.Br(),
        dcc.Link(html.Button("Submit!", id='submit-{}'.format(NAME),
                             n_clicks=0, className="btn btn-lg btn-primary btn-block"),
                 href=href(__name__, submit)),
    ], className="container", id='signup')


@app.callback(
    Output('signup', 'children'),
    [],
    [
        State('username-{}'.format(NAME), 'value'),
        State('email-{}'.format(NAME), 'value'),
        State('biography-{}'.format(NAME), 'value'),
        State('categories-{}'.format(NAME), 'value'),
        State('details-{}'.format(NAME), 'value'),
    ],
    [Event('submit-{}'.format(NAME), 'click')]
)
def submit_signup_information(username, email, biography, categories, details):
    database.identity.handle_signup_submit(username, email, biography, categories, details)
    session['username'] = username
