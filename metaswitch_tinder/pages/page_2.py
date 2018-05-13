import dash_html_components as html


def layout():
    return html.Div(
        children=[
            html.H1("Metaswitch Tinder loves you!")
        ],
        className="container",
        id="main",  # Must match the ID in the "startLoops" javascript function.
    )
