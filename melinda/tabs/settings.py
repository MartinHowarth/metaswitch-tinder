import logging

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output, State

from melinda.app import app
from melinda.components.grid import create_equal_row
from melinda.components.session import (
    current_user_email,
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
        username = get_current_user().name
    else:
        return html.Div([html.Br(), html.H1("You must be logged in to do this")])

    user = get_current_user()

    return html.Div(
        children=[
            html.H1("Hi {}! Want to update your details?".format(username)),
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
    [State(biography_id, "value")],
    [Event(save_id, "click")],
)
def set_mentor_tags(bio: str):
    """
    Callback that gets called when a tag is added or deleted

    :param bio: Biography of the users.
    """
    log.info("User %s set bio: %s", current_user_email(), bio)
    user = get_current_user()
    user.bio = bio
    user.commit()

    return "Saved!"


@app.callback(Output(_dummy1, "children"), [], [], [Event(delete_id, "click")])
def delete_account():
    """
    Callback that gets called when the user requests account deletion.
    """
    user = get_current_user()
    user_email = user.email
    log.info("User %s requested account deletion.", user_email)
    user.delete()
    log.info("User %s deleted.", user_email)
    logout()
