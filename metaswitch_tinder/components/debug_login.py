import dash_core_components as dcc
import dash_html_components as html
import logging

from dash.dependencies import Output, State, Event

from metaswitch_tinder.app import app
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components import session
from metaswitch_tinder.components.auth import authenticated_login_is_enabled, handle_login
from metaswitch_tinder.components.grid import create_equal_row


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '_')

debug_login_submit = 'submit'


def layout():
    """
    Layout for debug login.
    """
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
                 href=href(__name__, debug_login_submit)),
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
def submit_debug_login(username):
    log.info("%s - Signin clicked: %s", NAME, username)
    if authenticated_login_is_enabled():
        return "Debug logins are disabled."

    handle_login(username, '{}@email.com'.format(username))
    session.set_post_login_redirect(href(__name__, debug_login_submit))
