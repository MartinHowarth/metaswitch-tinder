import dash_html_components as html

from metaswitch_tinder.components.auth import is_logged_in, current_username


def layout():
    if is_logged_in():
        username = current_username()
    else:
        return html.Div([html.Br(),
                         html.H1("You must be logged in to do this")])
    return html.Div(
        children=[
            html.H1("{}, here are your messages".format(username))
        ],
        className="container",
    )
