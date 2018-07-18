import logging

from dash.dependencies import Input, Output

from melinda import tabs
from melinda.app import app
from melinda.components import session
from melinda.components.tabs import generate_tabs

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")

tabs_id = "tabs-{}".format(NAME)
display_id = "tab-display-{}".format(NAME)


def layout():
    cached_tab = session.get_last_tab_on(NAME) or "mentor_matches"

    return generate_tabs(
        {
            "Record some skills": "mentor_skills",
            "Your matches - mentees who have asked to learn from you": "mentor_matches",
        },
        default_tab=cached_tab,
        tabs_id=tabs_id,
        display_id=display_id,
    )


@app.callback(Output(display_id, "children"), [Input(tabs_id, "value")])
def display_tab(tab_name: str):
    """
    Callback that gets called when a tab is clicked.

    It is used to determine what html to display for the new url.
    :param tab_name: Name of the tab what was selected.
    :return: Dash html object to display as the children of the 'tab-content' Div.
    """
    # Cache the last tab we were on so the user returns to where they left off
    # if they navigate away and come back
    session.set_last_tab_on(NAME, tab_name)

    return tabs.tabs[tab_name]()
