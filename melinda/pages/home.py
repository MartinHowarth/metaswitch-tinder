import logging

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output

from melinda.app import app
from melinda.app_structure import href
from melinda.components import session
from melinda.components.about import about_div
from melinda.components.grid import create_equal_row

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")

im_a_mentee = "im_a_mentee"
im_a_mentor = "im_a_mentor"
signin = f"signin-{NAME}"


def layout():
    return html.Div(
        [
            html.H1("Melinda", className="cover-heading"),
            html.P(
                "Melinda is a match-making service for informal mentoring "
                "and pastoral support.",
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
