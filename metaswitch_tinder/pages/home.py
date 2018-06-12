import logging

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output

from metaswitch_tinder.app import app
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components import session
from metaswitch_tinder.components.about import about_div
from metaswitch_tinder.components.grid import create_equal_row

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")

im_a_mentee = "im_a_mentee"
im_a_mentor = "im_a_mentor"
signin = f"signin-{NAME}"


def layout():
    return html.Div(
        [
            html.H1("Metaswitch Tinder", className="cover-heading"),
            html.P(
                "Metaswitch Tinder is a match-making service for informal mentoring "
                "and unofficial pastoral support "
                "at Metaswitch.",
                className="lead",
            ),
            create_equal_row(
                [
                    dcc.Link(
                        "Become a mentor!",
                        href=href(__name__, im_a_mentor),
                        className="btn btn-lg btn-info",
                    ),
                    dcc.Link(
                        "Become a mentee!",
                        href=href(__name__, im_a_mentee),
                        className="btn btn-lg btn-primary",
                    ),
                ]
            ),
            html.Br(),
            html.Br(),
            html.A(
                "I have an account - sign in.",
                href="/login",
                className="btn btn-primary",
                id=signin,
            ),
            html.Br(),
            html.Br(),
            about_div(),
            html.Div(id="dummy", hidden=True),
        ],
        className="container text-center",
    )


@app.callback(Output("dummy", "children"), [], [], [Event(signin, "click")])
def submit_signup_information():
    log.debug("%s - Signin clicked", NAME)
    session.set_post_login_redirect(href(__name__, signin))
