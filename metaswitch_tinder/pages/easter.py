import dash_html_components as html
import random

from metaswitch_tinder.app_config import config


def layout():
    return html.Div(
        children=[
            html.Img(
                src=random.choice(config.ducks),
                style={'display': 'block',
                       'width': '100%',
                       'vertical-align': 'middle'}
            ),
        ],
    )
