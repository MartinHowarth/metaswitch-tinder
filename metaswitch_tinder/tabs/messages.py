import dash_html_components as html

from flask import session


def layout():
    print('messages', session)
    if 'username' in session:
        username = session['username']
    else:
        print('not logged in', session)
        return html.Div([html.Br(),
                         html.H1("You must be logged in to do this")])
    return html.Div(
        children=[
            html.H1("{}, here are your messages".format(username))
        ],
        className="container",
    )
