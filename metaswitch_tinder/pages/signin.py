import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event
from flask import session

from metaswitch_tinder import global_config
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder import database, pages


NAME = __name__.replace('.', '')


def signin_redirected(next_page):
    def signin():
        return html.Div([
            html.H1("Metaswitch Tinder", className="text-center"),
            html.Br(),
            create_equal_row([
                html.Label('Username:', className="text-center"),
                dcc.Input(value='', type='text', id='username-{}'.format(NAME)),
            ]),
            html.Br(),
            html.Button("Submit!", id='submit-{}'.format(NAME),
                        n_clicks=0, className="btn btn-lg btn-primary btn-block"),
            html.Div(next_page, id='next-page', style={'display': 'none'})
        ],
            className="container", id='signin')
    return signin


def add_callbacks(app):
    @app.callback(
        Output('signin', 'children'),
        [],
        [
            State('username-{}'.format(NAME), 'value'),
            State('next-page', 'children'),
        ],
        [Event('submit-{}'.format(NAME), 'click')]
    )
    def submit_signup_information(username, next_page):
        print('signin', session)
        database.identity.handle_signin_submit(username)
        print('signin', session)
        session['username'] = username
        print('signin', session)
        return pages.pages[next_page]()
