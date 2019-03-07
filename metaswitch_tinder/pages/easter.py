import random

import dash_html_components as html

from metaswitch_tinder.app_config import config


def layout():
    return html.Div(
        children=[
            html.Img(
                src=random.choice(config.ducks),
                style={"display": "block", "width": "100%", "vertical-align": "middle"},
            )
        ]
    )
