import dash_core_components as dcc
import dash_html_components as html

from flask import session


def messages():
    print('messages', session)
    username = session.get('username', 'Not logged in!')
    return html.Div(
        children=[
            html.H1("{}, here are your messages".format(username))
        ],
        className="container",
    )
