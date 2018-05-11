import dash_core_components as dcc
import dash_html_components as html

from flask import session

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder import global_config


def messages(config: MetaswitchTinder):
    return html.Div(
        children=[
            html.H1("{}, here are your messages".format(session['username']))
        ],
        className="container",
        id="main",  # Must match the ID in the "startLoops" javascript function.
    )
