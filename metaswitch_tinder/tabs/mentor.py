import logging

from dash.dependencies import Input, Output

from metaswitch_tinder import tabs
from metaswitch_tinder.app import app
from metaswitch_tinder.components.tabs import generate_tabs


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '')

tabs_id = 'tabs-{}'.format(NAME)
display_id = 'tab-display-{}'.format(NAME)


def layout():
    return generate_tabs(
        {
            'Record some skills': 'mentor_skills',
            'Your matches - mentees who have asked to learn from you': 'mentor_matches',
        },
        default_tab='mentor_matches',
        tabs_id=tabs_id,
        display_id=display_id
    )


@app.callback(Output(display_id, 'children'),
              [Input(tabs_id, 'value')])
def display_tab(tab_name: str):
    """
    Callback that gets called when a tab is clicked.

    It is used to determine what html to display for the new url.
    :param tab_name: Name of the tab what was selected.
    :return: Dash html object to display as the children of the 'tab-content' Div.
    """
    return tabs.tabs[tab_name]()
