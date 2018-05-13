import dash_html_components as html
import random

from metaswitch_tinder.app import config


def layout():
    return html.Div(
        children=[
            html.H1("Hello from Metaswitch Tinder!", className="cover-heading"),
            html.Img(src=random.choice(config.serious_ducks), className="rounded-circle", width=200, height=200),
            html.P("This page has some examples of how we want things to look", className="lead"),
            html.Button("Wide Button Example", className="btn btn-primary btn-lg btn-block")
        ],
        className="container text-center",
        id="main",  # Must match the ID in the "startLoops" javascript function.
    )
