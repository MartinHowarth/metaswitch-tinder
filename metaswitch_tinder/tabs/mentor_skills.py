import dash_core_components as dcc
import dash_html_components as html
import logging

from dash.dependencies import Input, Output
from typing import List

from metaswitch_tinder import database
from metaswitch_tinder.app import app
from metaswitch_tinder.components.session import current_username, current_user
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '_')

categories_id = 'categories-{}'.format(NAME)


def layout():
    user = current_user()

    return html.Div([
        create_equal_row([html.Label('Tell us what you know about:')]),
        multi_dropdown_with_tags(database.tags.get_tags(), categories_id,
                                 init_selection=user.tags),
        html.Br(),
        create_equal_row([html.Label('Additional topic tags:')]),
        create_equal_row(
            [dcc.Input(placeholder='e.g. \"python\", \"object-oriented design\", \"session-based testing\"',
                       value='', type='text', id='details-{}'.format(NAME))]),
        html.Div(id='dummy-{}'.format(NAME), hidden=True)
    ],
        className="container")


@app.callback(Output('dummy-{}'.format(NAME), 'children'),
              [
                  Input(categories_id, 'value')
              ])
def set_mentor_tags(tags: List[str]):
    """
    Callback that gets called when a tag is added or deleted

    :param tags: List of tags, comma separated.
    """
    log.info("User %s set mentor tags: %s", current_username(), tags)
    current_user().set_tags(tags)
