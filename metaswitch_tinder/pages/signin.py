import dash_core_components as dcc
import dash_html_components as html
import logging

from dash.dependencies import Output, State, Event

import metaswitch_tinder.database.models

from metaswitch_tinder.app import app
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components import session
from metaswitch_tinder.components.grid import create_equal_row


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '_')

submit = 'submit'


def layout():
    return html.Div([
        html.H1("Metaswitch Tinder", className="text-center"),
        html.Br(),
        create_equal_row([
            html.Label('Username:', className="text-center"),
            dcc.Input(value='', type='text', id='username-{}'.format(NAME)),
        ]),
        html.Br(),
        dcc.Link(html.Button("Submit!", id='submit-{}'.format(NAME),
                             n_clicks=0, className="btn btn-lg btn-primary btn-block"),
                 href=href(__name__, submit)),
    ],
        className="container", id='signin')


@app.callback(
    Output('signin', 'children'),
    [],
    [
        State('username-{}'.format(NAME), 'value'),
    ],
    [Event('submit-{}'.format(NAME), 'click')]
)
def submit_signup_information(username):
    log.info("%s - Signin clicked: %s", NAME, username)
    metaswitch_tinder.database.models.handle_signin_submit(username)
    session.login(username)
