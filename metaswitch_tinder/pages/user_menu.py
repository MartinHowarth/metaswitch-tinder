import logging
import dash_html_components as html

from dash.dependencies import Input, Output

from metaswitch_tinder import tabs
from metaswitch_tinder.app import app
from metaswitch_tinder.components.session import wait_for_login, set_on_mentee_tab
from metaswitch_tinder.components.tabs import generate_tabs


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '')

tabs_id = 'tabs-{}'.format(NAME)
display_id = 'tab-display-{}'.format(NAME)


def layout():
    wait_for_login()
    return html.Div([generate_tabs(
        {
            'Messages': 'messages',
            'Be a mentee': 'mentee',
            'Be a mentor': 'mentor',
            'Settings': 'settings'
        },
        default_tab='mentee',
        tabs_id=tabs_id,
        display_id=display_id
    )],
        style={
        'width': '80%',
        'margin-left': 'auto',
        'margin-right': 'auto'
        })


@app.callback(Output(display_id, 'children'),
              [Input(tabs_id, 'value')])
def display_tab(tab_name):
    """
    Callback that gets called when a tab is clicked.

    It is used to determine what html to display for the new url.
    :param tab_name: Name of the tab what was selected.
    :return: Dash html object to display as the children of the 'tab-content' Div.
    """
    if tab_name == 'mentee':
        set_on_mentee_tab(True)
    else:
        set_on_mentee_tab(False)

    return tabs.tabs[tab_name]()
