import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Output, State, Event

import metaswitch_tinder.database.matches

from metaswitch_tinder.app import app
from metaswitch_tinder import database
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components.session import wait_for_login, current_username
from metaswitch_tinder.components.grid import create_equal_row
from metaswitch_tinder.components.inputs import multi_dropdown_with_tags


NAME = __name__.replace('.', '')
submit_request = 'submit_request'

categories_id = 'categories-{}'.format(NAME)
details_id = 'details-{}'.format(NAME)
submit_button = 'submit-{}'.format(NAME)


def layout():
    return html.Div([
        html.Label('What topics do you want to learn about?'),
        html.Br(),
        multi_dropdown_with_tags(database.tags.get_tags(), categories_id),
        html.Br(),
        html.Label('Any additional details about this request that the mentor should know?', className="text-center"),
        html.Br(),
        create_equal_row([dcc.Textarea(value='', id=details_id)]),
        html.Br(),
        dcc.Link(html.Button("Submit my request!",
                             id=submit_button,
                             className="btn btn-lg btn-success btn-block"),
                 href=href(__name__, submit_request)),
    ],
        className="container", id='mentee-request-div')


@app.callback(
    Output('mentee-request-div'.format(NAME), 'children'),
    [],
    [
        State(categories_id, 'value'),
        State(details_id, 'value'),
    ],
    [Event(submit_button, 'click')]
)
def submit_mentee_information(categories, details):
    print('mentee request', categories, details)
    wait_for_login()
    metaswitch_tinder.database.matches.handle_mentee_add_request(current_username(), categories, details)
