import logging
from typing import List

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from metaswitch_tinder.app import app
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import tags_dropdown_with_add_new_entry_box
from metaswitch_tinder.components.session import current_username, get_current_user

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")

categories_id = "categories-{}".format(NAME)


def layout():
    user = get_current_user()

    return html.Div(
        [
            create_equal_row([html.Label("Tell us what you know about:")]),
            *tags_dropdown_with_add_new_entry_box(
                categories_id, init_selection=user.tags
            ),
            html.Br(),
            create_equal_row([html.Label("Additional details about your skills:")]),
            create_equal_row(
                [dcc.Input(value="", type="text", id="details-{}".format(NAME))]
            ),
            html.Div(id="dummy-{}".format(NAME), hidden=True),
        ],
        className="container",
    )


@app.callback(
    Output("dummy-{}".format(NAME), "children"), [Input(categories_id, "value")]
)
def set_mentor_tags(tags: List[str]):
    """
    Callback that gets called when a tag is added or deleted

    :param tags: List of tags, comma separated.
    """
    log.info("User %s set mentor tags: %s", current_username(), tags)
    get_current_user().set_tags(tags)
