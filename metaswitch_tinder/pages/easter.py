import dash_core_components as dcc
import dash_html_components as html
import random

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder import global_config


def easter():
    return html.Div(
        children=[
            html.Img(
                src=random.choice(global_config.Global.CONFIG.ducks),
                style={'display': 'block',
                       'width': '100%',
                       'vertical-align': 'middle'}
            ),
        ],
    )
