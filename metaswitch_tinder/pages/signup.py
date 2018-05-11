import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder import global_config
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder import database


NAME = __name__.replace('.', '')


def signup_redirected(next_page):
    def signup(config: MetaswitchTinder=None):
        return html.Div([
            html.H1("Metaswitch Tinder", className="text-center"),
            html.Br(),
            create_equal_row([
                html.Label('Username:', className="text-center"),
                dcc.Input(value='', type='text', id='username-{}'.format(NAME)),
            ]),
            html.Br(),
            create_equal_row([
                html.Label('Email:', className="text-center"),
                dcc.Input(value='@metaswitch.com', type='text', id='email-{}'.format(NAME)),
            ]),
            html.Br(),
            create_equal_row([
                html.Label('Biography:', className="text-center"),
                dcc.Input(value='Loves ducks', type='text', id='biography-{}'.format(NAME)),
            ]),
            html.Br(),
            html.A(html.Button("Submit!", id='submit-{}'.format(NAME),
                               n_clicks=0, className="btn btn-lg btn-primary btn-block"),
                   href=next_page)
        ],
            className="container", id='signup')
    return signup


def add_callbacks(app):
    @app.callback(
        Output('signup', 'children'),
        [],
        [
            State('username-{}'.format(NAME), 'value'),
            State('email-{}'.format(NAME), 'value'),
            State('biography-{}'.format(NAME), 'value'),
        ],
        [Event('submit-{}'.format(NAME), 'click')]
    )
    def submit_signup_information(username, email, biography):
        global_config.Global.USERNAME = username
        database.input.handle_signup_submit(username, email, biography)
        return
