import dash_core_components as dcc
import dash_html_components as html
import logging

from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components.grid import create_equal_row


log = logging.getLogger(__name__)

signin = 'signin'
signup = 'signup'


def layout():
    return html.Div([
        html.H1("Metaswitch Tinder", className="cover-heading"),
        create_equal_row([
            dcc.Link("Sign in!", href=href(__name__, signin), className="btn btn-lg btn-secondary"),
            dcc.Link("Sign up!", href=href(__name__, signup), className="btn btn-lg btn-primary"),
        ])
    ],
        className="container text-center",)
