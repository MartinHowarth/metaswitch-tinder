import dash_core_components as dcc
import dash_html_components as html
import random

from metaswitch_tinder import global_config


def page_1():
    return html.Div(
        children=[
            html.H1("Hello from Metaswitch Tinder!", className="cover-heading"),
            html.Img(src=random.choice(global_config.Global.CONFIG.serious_ducks), className="rounded-circle", width=200, height=200),
            html.P("This page has some examples of how we want things to look", className="lead"),
            html.Button("Wide Button Example", className="btn btn-primary btn-lg btn-block")
        ],
        className="container text-center",
        id="main",  # Must match the ID in the "startLoops" javascript function.
    )
