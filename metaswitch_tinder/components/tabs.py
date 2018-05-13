import dash_core_components as dcc
import dash_html_components as html

from typing import Dict


def generate_tabs(tabs: Dict[str, html.Div], default_tab: html.Div, tabs_id: str, display_id: str) -> html.Div:
    """
    :param tabs: Dict of {"tab_name": html.Div(tab contents)}
    :param default_tab: The default tab (by name) to display
    :param tabs_id: The id of the tabs container.
    :param display_id: The id of the Div that will contain the tab contents.
    :return: html.Div for the tabs.
    """
    formatted_dict = [
        {'label': key, 'value': value} for key, value in tabs.items()
    ]

    return html.Div([
        dcc.Tabs(
            tabs=formatted_dict,
            value=default_tab,
            id=tabs_id,
        ),
        html.Div(id=display_id)
    ])
