import logging

from typing import List

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output, State

from metaswitch_tinder.app import app
from metaswitch_tinder.components.inputs import tags_dropdown_with_add_new_entry_box
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.session import (
    current_username,
    get_current_user,
    is_logged_in,
)
from metaswitch_tinder.database.models import Request, get_request_by_id


from metaswitch_tinder.app_structure import href

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")

edit_id = "edit-{}".format(NAME) + "-{}"
tags_id = "tags-{}".format(NAME)
details_id = "details-{}".format(NAME)
save_id = "save-{}".format(NAME)
delete_id = "delete-{}".format(NAME)
current_request_id = "current_request-{}".format(NAME)

MAX_REQUESTS = 20  # The maximum number of request edit buttons that will be shown.


def children_no_requests():
    return [
        html.H1("You have no open requests."),
        html.Div(id=save_id, hidden=True),
        html.Div(id=delete_id, hidden=True),
    ]


def children_requests(requests: List[Request]) -> List:
    table_rows = [
        html.Tr(
            [
                html.Td("Topics"),
                html.Td("Request details"),
                html.Td("Number of possible mentors"),
                html.Td(),
            ],
            className="table-active",
        )
    ]

    for ii, request in enumerate(requests):
        edit_button = html.Button(
            "Edit", id=edit_id.format(ii), className="btn btn-info btn-block"
        )

        table_rows.append(
            html.Tr(
                [
                    html.Td(", ".join(request.tags)),
                    html.Td(request.comment),
                    html.Td(len(request.possible_mentors)),
                    html.Td(edit_button),
                ],
                className="table-light",
            )
        )

    elements = [
        html.Table([*table_rows], className="table table-condensed"),
        html.Div(id=save_id, hidden=True),
        html.Div(id=delete_id, hidden=True),
    ]
    remaining_buttons = [
        html.Button(
            "Edit",
            id=edit_id.format(n + len(requests)),
            className="btn btn-info btn-block",
            hidden=True,
        )
        for n in range(MAX_REQUESTS - len(requests))
    ]
    elements.extend(remaining_buttons)
    return elements


def layout():
    """Main layout for the open requests tab."""
    if is_logged_in():
        user = get_current_user()
    else:
        return html.Div([html.Br(), html.H1("You must be logged in to do this")])

    requests = user.get_requests()  # type: List[Request]

    if not requests:
        children = children_no_requests()
    else:
        children = children_requests(requests)

    children.append(html.Div(id=current_request_id, hidden=True))

    return html.Div(children=children, className="container", id=NAME)


def edit_request_layout(request: Request):
    """Layout to display when a request has been selected to be edited."""
    log.debug("Displaying request edit page for request: %s", request)
    return html.Div(
        [
            html.Label("What topics do you want to learn about?"),
            html.Br(),
            *tags_dropdown_with_add_new_entry_box(tags_id, init_selection=request.tags),
            html.Br(),
            html.Label(
                "Any additional details about this request that the mentor "
                "should know?",
                className="text-center",
            ),
            html.Br(),
            create_equal_row([dcc.Textarea(value=request.comment, id=details_id)]),
            html.Br(),
            dcc.Link(
                html.Button(
                    "Save",
                    id=save_id,
                    n_clicks=0,
                    className="btn btn-lg btn-primary btn-block",
                ),
                href=href(__name__, save_id),
            ),
            html.Br(),
            html.Br(),
            dcc.Link(
                html.Button(
                    "Delete Request",
                    id=delete_id,
                    n_clicks=0,
                    className="btn btn-lg btn-warning btn-block",
                ),
                href=href(__name__, delete_id),
            ),
            html.Div(request.id, id=current_request_id, hidden=True),
        ],
        className="container",
    )


def get_request_id_by_index(index: int) -> str:
    """Get the request of the current user by numerical index."""
    return get_current_user().requests[index]


states = [State(edit_id.format(n), "id") for n in range(MAX_REQUESTS)]
states.extend([State(edit_id.format(n), "n_clicks") for n in range(MAX_REQUESTS)])
events = [Event(edit_id.format(n), "click") for n in range(MAX_REQUESTS)]


@app.callback(Output(NAME, "children"), [], states, events)
def handle_edit_button_press(*args):
    """
    Handle any of the edit buttons being pressed.

    Determines which of the buttons was pressed, and then displays the user the editing
    page for the corresponding request.
    """
    edit_clicks = args[:MAX_REQUESTS]
    edit_ids = args[MAX_REQUESTS:]

    index = 0
    for _id, n_click in zip(edit_clicks, edit_ids):
        if n_click:
            index = int(_id.split("-")[-1])
            log.debug("Request edit button index %s was clicked.", index)
            break

    request_id = get_request_id_by_index(index)
    return edit_request_layout(get_request_by_id(request_id))


@app.callback(
    Output(current_request_id, "children"),
    [],
    [
        State(current_request_id, "children"),
        State(tags_id, "value"),
        State(details_id, "value"),
        State(save_id, "n_clicks"),
        State(delete_id, "n_clicks"),
    ],
    [Event(save_id, "click"), Event(delete_id, "click")],
)
def handle_save_and_delete(
    request_id: str, tags: List[str], details: str, n_save_clicked, n_delete_clicked
):
    """Handles the user clicking save or delete on the request editing page."""
    log.debug(
        "Handling request update or deletion: %s, %s", n_save_clicked, n_delete_clicked
    )
    current_request = get_request_by_id(request_id)
    if current_request is None:
        raise RuntimeError(
            "Unrecognised request ID passed to editing page: %s" % request_id
        )
    if n_save_clicked:
        current_request.tags = tags
        current_request.comment = details
        current_request.commit()
        log.info("User %s updated request: %s", current_username(), current_request)
    elif n_delete_clicked:
        log.info("User %s deleted request: %s", current_username(), current_request)
        current_request.delete()
