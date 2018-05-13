import dash_core_components as dcc
import dash_html_components as html
import logging

from flask import session

from metaswitch_tinder import database
from metaswitch_tinder.components.auth import is_logged_in, current_username
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '')


def layout():
    print('settings', session)
    if is_logged_in():
        username = current_username()
    else:
        return html.Div([html.Br(),
                         html.H1("You must be logged in to do this")])
    return html.Div(
        children=[
            html.H1("Hi {}! Want to update your details?".format(username),),
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
            dcc.Textarea(placeholder='Enter a biography', value='', id='biography-{}'.format(NAME),
                         style={'width': '100%'}),
            html.Br(),
            create_equal_row([html.Label('Mentoring topics:')]),
            multi_dropdown_with_tags(database.tags.get_tags(), 'categories-{}'.format(NAME)),
            html.Br(),
            create_equal_row([html.Label('Additional topic tags:')]),
            create_equal_row(
                [dcc.Input(placeholder='e.g. \"python\", \"object-oriented design\", \"session-based testing\"',
                           value='', type='text', id='details-{}'.format(NAME))]),
            html.Br(),
            html.Button("Save", id='submit-{}'.format(NAME),
                        n_clicks=0, className="btn btn-lg btn-primary btn-block"),
            html.Button("Delete Account", id='submit-{}'.format(NAME),
                        n_clicks=0, className="btn btn-lg btn-warning btn-block"),
        ],
        className="container",
    )
