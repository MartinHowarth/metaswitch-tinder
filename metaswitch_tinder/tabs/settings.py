import logging

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output, State

from metaswitch_tinder.app import app
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.session import (
    current_username,
    get_current_user,
    is_logged_in,
    logout,
)

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")

biography_id = "biography-{}".format(NAME)
email_id = "email-{}".format(NAME)
save_id = "save-{}".format(NAME)
delete_id = "delete-{}".format(NAME)
_dummy1 = "dummy1-{}".format(NAME)


def layout():
    if is_logged_in():
        username = current_username()
    else:
        return html.Div([html.Br(), html.H1("You must be logged in to do this")])

    user = get_current_user()

    return html.Div(
        children=[
            html.H1("Hi {}! Want to update your details?".format(username)),
            html.Br(),
            create_equal_row(
                [
                    html.Label("Email:"),
                    dcc.Input(value=user.email, type="text", id=email_id),
                ]
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
                value=user.bio,
                id=biography_id,
                style={"width": "100%"},
            ),
            html.Br(),
            html.Button(
                "Save",
                id=save_id,
                n_clicks=0,
                className="btn btn-lg btn-primary btn-block",
            ),
            html.Br(),
            html.Br(),
            dcc.Link(
                html.Button(
                    "Delete Account",
                    id=delete_id,
                    n_clicks=0,
                    className="btn btn-lg btn-warning btn-block",
                ),
                href="/",
            ),
            html.Div(id=_dummy1, hidden=True),
        ],
        className="container",
    )


@app.callback(
    Output(save_id, "children"),
    [],
    [State(biography_id, "value"), State(email_id, "value")],
    [Event(save_id, "click")],
)
def set_mentor_tags(bio: str, email: str):
    """
    Callback that gets called when a tag is added or deleted

    :param bio: Biography of the users.
    :param email: User email address.
    """
    log.info("User %s set bio: %s", current_username(), bio)
    log.info("User %s set email: %s", current_username(), email)
    user = get_current_user()
    user.bio = bio
    user.email = email
    user.commit()

    return "Saved!"


@app.callback(Output(_dummy1, "children"), [], [], [Event(delete_id, "click")])
def delete_account():
    """
    Callback that gets called when the user requests account deletion.
    """
    user = get_current_user()
    log.info("User %s requested account deletion.", user.name)
    user.delete()
    log.info("User %s deleted.", user.name)
    logout()
