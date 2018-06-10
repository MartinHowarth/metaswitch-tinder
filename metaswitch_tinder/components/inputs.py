import logging
from typing import List

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Event, Output, State

from metaswitch_tinder.app import app
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.database.models import Tag, list_all_tags
from metaswitch_tinder.components.session import current_username

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")


new_tag_id = "new-tag-{}".format(NAME)
ok_id = "ok-{}".format(NAME)


def tags_dropdown_with_add_new_entry_box(
    _id: str, init_selection: List[str] = None
) -> List:

    tag_list = [{"label": tag.name, "value": tag.name} for tag in list_all_tags()]

    return [
        dcc.Dropdown(options=tag_list, value=init_selection or [], multi=True, id=_id),
        html.Br(),
        create_equal_row(
            [
                html.Label("Create a new tag:"),
                dcc.Input(value="", type="text", id=new_tag_id),
                html.Button("Ok", id=ok_id, className="btn btn-success btn-block"),
            ]
        ),
    ]


@app.callback(
    Output(ok_id, "children"), [], [State(new_tag_id, "value")], [Event(ok_id, "click")]
)
def handle_new_tag_creation(new_tag_str: str):
    """
    Handles the user clicking Ok to submit a new tag.

    Return value of this sets the text on the Ok button.
    """
    log.debug("User %s creating new tag: %s", current_username(), new_tag_str)

    if not new_tag_str:
        # If the user didn't enter anything, do nothing.
        return "Ok"

    if new_tag_str in [tag.name for tag in list_all_tags()]:
        return "Tag Exists"

    if Tag.normalise_tag(new_tag_str) == new_tag_str:
        # Tag is acceptable, enter it into the database.
        new_tag = Tag(new_tag_str)
        new_tag.add()
        return "Ok"

    # If it's unacceptable, then the other callback will have changed the input
    # field to be an acceptable value.
    return "Normalised to {0!r}, click again to accept.".format(
        Tag.normalise_tag(new_tag_str)
    )


@app.callback(
    Output(new_tag_id, "value"),
    [],
    [State(new_tag_id, "value")],
    [Event(ok_id, "click")],
)
def handle_new_tag_creation_input_field(new_tag_str: str):
    """
    Handles the user clicking Ok to submit a new tag.

    Return value of this function sets the text in the entry field.
    """
    if new_tag_str in [tag.name for tag in list_all_tags()]:
        # Tag already exists.
        return ""

    if Tag.normalise_tag(new_tag_str) != new_tag_str:
        # If the tag isn't acceptable, put the normalised tag in the input field.
        return Tag.normalise_tag(new_tag_str)

    # If it is acceptable, clear the input field.
    return ""
