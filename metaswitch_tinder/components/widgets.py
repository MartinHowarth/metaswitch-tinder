import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State, Event
from flask import session


def logout_button():
    return html.A(html.Button("Logout", id='logout',
                              className="btn btn-primary btn-block btn-warning"),
                  href='/', id='dummy')


def report_button():
    return html.A(html.Button("Report", id='report',
                              className="btn btn-primary btn-block btn-danger"),
                  href='/', id='dummy')


def add_callbacks(app):
    @app.callback(
        Output('dummy', 'children'),
        [],
        [],
        [Event('logout', 'click')]
    )
    def handle_logout():
        print("log out")
        del session['username']
        del session['is_mentee']
        return
