import logging
from typing import List, Tuple

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, State

log = logging.getLogger(__name__)


def logout_button():
    return dcc.Link(
        html.Button(
            "Logout", id="logout", className="btn btn-primary btn-block btn-warning"
        ),
        href="/",
        id="logout",
    )


def set_page_content() -> Output:
    return Output("page-content", "children")


def set_hidden_information(key: str, value: str) -> html.Div:
    """Define a html element to store a value by key. The element is invisible."""
    return html.Div(value, id=key, hidden=True)


def get_hidden_information(key: str) -> State:
    """
    Dash `State` object to get a value by key.

    Information must have been previously stored by `set_hidden_information`.
    """
    return State(key, "children")


def get_num_button_clicks(button_id: str) -> State:
    """Dash `State` object to get the number of times a button was clicked."""
    return State(button_id, "n_clicks")


def choose_page(btn_click_list: List[Tuple[int, str]]) -> str:
    """
    Given a list of tuples of (num_clicks, next_page) choose the next_page that
    corresponds to exactly 1 num_clicks.

    This is to help with deciding which page to go to next when clicking on one
    of many buttons on a page.

    The expectation is that exactly one button will have been clicked, so we get
    a deterministic next page.

    :param btn_click_list: List of tuples of (num_clicks, next_page).
    :return: The id of the next page.
    """
    for tup in btn_click_list:
        if tup[0] == 1:
            return tup[1]
    raise ValueError(
        "No clicks were detected, or the click list is misconfigured: {}".format(
            btn_click_list
        )
    )
