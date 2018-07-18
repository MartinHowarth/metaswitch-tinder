import logging

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output

from melinda.app import app
from melinda.app_structure import href
from melinda.components import session
from melinda.components.grid import create_equal_row
from melinda.pages import user_menu
from melinda.tabs import mentor

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")

signin = "signin"
signup = "signup"


def layout():
    return html.Div(
        [
            html.H1("Melinda", className="cover-heading"),
            create_equal_row(
                [
                    html.A(
                        "Sign in!",
                        href="/login",
                        id="signin-{}".format(NAME),
                        className="btn btn-lg btn-secondary",
                    ),
                    dcc.Link(
                        "Sign up!",
                        href=href(__name__, signup),
                        className="btn btn-lg btn-primary",
                    ),
                ]
            ),
        ],
        className="container text-center",
        id="signin-or-signup",
    )


@app.callback(
    Output("signin-or-signup", "children"),
    [],
    [],
    [Event("signin-{}".format(NAME), "click")],
)
def submit_signup_information():
    log.info("%s - Signin clicked", NAME)

    # Make the default tab the mentor skills tab when signing in
    # as a mentor.
    session.set_last_tab_on(user_menu.NAME, "mentor")
    session.set_last_tab_on(mentor.NAME, "mentor_skills")
    session.set_post_login_redirect(href(__name__, signin))
