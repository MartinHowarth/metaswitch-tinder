import logging

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output, State

from metaswitch_tinder.app import app
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components import session
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import tags_dropdown_with_add_new_entry_box

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")

submit = "submit"


def layout():
    return html.Div(
        [
            html.H1("Metaswitch Tinder", className="text-center"),
            html.Br(),
            html.P(
                "Username and email provided by google authentication.",
                className="lead",
            ),
            html.Br(),
            create_equal_row(
                [
                    html.Label("Location:"),
                    dcc.Input(
                        value="",
                        placeholder="Which office are you in?",
                        type="text",
                        id="location-{}".format(NAME),
                    ),
                ]
            ),
            html.Br(),
            create_equal_row([html.Label("Biography:")]),
            dcc.Textarea(
                placeholder="Enter a biography",
                value="",
                id="biography-{}".format(NAME),
                style={"width": "100%"},
            ),
            html.Br(),
            create_equal_row([html.Label("Tell us what you know about:")]),
            *tags_dropdown_with_add_new_entry_box("categories-{}".format(NAME)),
            html.Br(),
            create_equal_row([html.Label("Additional details about your skills:")]),
            create_equal_row(
                [dcc.Input(value="", type="text", id="details-{}".format(NAME))]
            ),
            html.Br(),
            html.A(
                html.Button(
                    "Submit!",
                    id="submit-{}".format(NAME),
                    n_clicks=0,
                    className="btn btn-lg btn-primary btn-block",
                ),
                href="/login",
            ),
        ],
        className="container",
        id="signup",
    )


@app.callback(
    Output("signup", "children"),
    [],
    [
        State("biography-{}".format(NAME), "value"),
        State("categories-{}".format(NAME), "value"),
        State("details-{}".format(NAME), "value"),
    ],
    [Event("submit-{}".format(NAME), "click")],
)
def submit_signup_information(biography, categories, details):
    session.store_signup_information(
        biography, mentor_categories=categories, mentor_details=details
    )
    session.set_post_login_redirect(href(__name__, submit))
