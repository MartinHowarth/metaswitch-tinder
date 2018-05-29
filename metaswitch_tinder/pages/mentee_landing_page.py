import dash_html_components as html
import logging

from dash.dependencies import Output, Event

from metaswitch_tinder.app import app
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components import session

from . import mentee_request


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '_')

sign_in = 'sign_in'


def layout():
    if session.is_logged_in():
        is_signed_in_fields = [
            html.H3("Welcome {}!".format(session.current_username()),
                    className="text-center"),
            html.Br(),
            html.Br(),
            html.H3('New mentoring request', className="text-center"),
        ]
    else:
        is_signed_in_fields = [
            html.H3('Existing Users', className="text-center"),
            html.A("Sign in!", href='/login', id='signin-{}'.format(NAME),
                   className="btn btn-lg btn-primary btn-block"),
            html.Br(),
            html.Br(),
            html.H3('New mentoring request', className="text-center"),
        ]

    return html.Div([
        html.H1("Metaswitch Tinder", className="text-center"),
        html.Br(),
        *is_signed_in_fields,
        html.Br(),
        mentee_request.layout(),
        html.Div(id='dummy-signin-{}'.format(NAME), hidden=True)
    ],
        className="container", id='my-div')


@app.callback(
    Output('my-div'.format(NAME), 'children'),
    [],
    [],
    [Event(mentee_request.submit_button, 'click')]
)
def submit_mentee_information():
    log.debug("%s - %a clicked", NAME, mentee_request.submit_button)
    session.set_post_login_redirect(href(__name__, mentee_request.submit_request))


@app.callback(
    Output('dummy-signin-{}'.format(NAME), 'children'),
    [],
    [],
    [Event('signin-{}'.format(NAME), 'click')]
)
def submit_signup_information():
    log.debug("%s - %s clicked", NAME, 'signin-{}'.format(NAME))
    session.set_post_login_redirect(href(__name__, sign_in))
