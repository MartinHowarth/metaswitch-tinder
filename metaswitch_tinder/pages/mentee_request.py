import logging
from typing import List

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output, State

from metaswitch_tinder import database
from metaswitch_tinder.app import app
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components import session
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags

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
            multi_dropdown_with_tags(database.get_tags(), categories_id),
            html.Br(),
            html.Label(
                "Any additional details about this request that the mentor "
                "should know?",
                className="text-center",
            ),
            html.Br(),
            create_equal_row([dcc.Textarea(value="", id=details_id)]),
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
        database.models.create_request(session.current_username(), categories, details)
    else:
        session.store_signup_information(
            "", request_categories=categories, request_details=details
        )
        session.set_post_login_redirect(href(__name__, submit_request))
