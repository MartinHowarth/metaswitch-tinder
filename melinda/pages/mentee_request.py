import logging
from typing import List

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output, State

from melinda import database
from melinda.app import app
from melinda.app_structure import href
from melinda.components import session
from melinda.components.grid import create_equal_row
from melinda.components.inputs import tags_dropdown_with_add_new_entry_box

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")

submit_request = "submit_request"

categories_id = "categories-{}".format(NAME)
details_id = "details-{}".format(NAME)
submit_button = "submit-{}".format(NAME)


def layout():
    if session.is_logged_in():
        log.debug("%s: already logged in.", NAME)
        btn = (
            dcc.Link(
                html.Button(
                    "Submit my request!",
                    id=submit_button,
                    className="btn btn-lg btn-success btn-block",
                ),
                href=href(__name__, submit_request),
            ),
        )
    else:
        log.debug("%s: not logged in.", NAME)
        btn = (
            html.A(
                html.Button(
                    "Submit my request and sign up!",
                    id=submit_button,
                    className="btn btn-lg btn-success btn-block",
                ),
                href="/login",
            ),
        )

    return html.Div(
        [
            html.Label("What topics do you want to learn about?"),
            html.Br(),
            *tags_dropdown_with_add_new_entry_box(categories_id),
            html.Br(),
            html.Label(
                "Describe in more detail what you're looking for:",
                className="text-center text-dark",
            ),
            html.Br(),
            create_equal_row(
                [
                    dcc.Textarea(
                        value="",
                        id=details_id,
                        rows=6,
                        placeholder="Try starting with one of the following:\n"
                        "  I'd like a code review of...\n"
                        "  I'd like weekly mentoring sessions...\n"
                        "  I'm looking for a one off education session about...\n"
                        "  I want a running partner.\n"
                        "  I'm looking for someone to play chess with.",
                        maxLength=2000,
                    )
                ]
            ),
            html.Br(),
            html.Div(btn),
            html.Div(id="dummy-submit-{}".format(NAME)),
        ],
        className="container",
        id="mentee-request-div",
    )


@app.callback(
    Output("dummy-submit-{}".format(NAME), "children"),
    [],
    [State(categories_id, "value"), State(details_id, "value")],
    [Event(submit_button, "click")],
)
def submit_mentee_information(categories: List[str], details: str):
    print("mentee request", categories, details)

    if session.is_logged_in():
        database.models.create_request(
            session.current_user_email(), categories, details
        )
    else:
        session.store_signup_information(
            "", request_categories=categories, request_details=details
        )
        session.set_post_login_redirect(href(__name__, submit_request))
