import dash_core_components as dcc
import dash_html_components as html
import logging

from dash.dependencies import Event, Output, State

from metaswitch_tinder.app import app
from metaswitch_tinder.components.session import is_logged_in, current_username, current_user
from metaswitch_tinder.components.grid import create_equal_row


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '')

biography_id = 'biography-{}'.format(NAME)
email_id = 'email-{}'.format(NAME)
submit_id = 'submit-{}'.format(NAME)


def layout():
    if is_logged_in():
        username = current_username()
    else:
        return html.Div([html.Br(),
                         html.H1("You must be logged in to do this")])

    user = current_user()

    return html.Div(
        children=[
            html.H1("Hi {}! Want to update your details?".format(username)),
            html.Br(),
            create_equal_row([
                html.Label('Email:'),
                dcc.Input(value=user.email, type='text', id=email_id),
            ]),
            html.Br(),
            create_equal_row([
                html.Label('Location:', ),
                dcc.Input(value='', placeholder='Which office are you in?', type='text', id='location-{}'.format(NAME)),
            ]),
            html.Br(),
            create_equal_row([html.Label('Biography:')]),
            dcc.Textarea(placeholder='Enter a biography', value=user.bio, id=biography_id,
                         style={'width': '100%'}),
            html.Br(),
            html.Button("Save", id=submit_id,
                        n_clicks=0, className="btn btn-lg btn-primary btn-block"),
            html.Button("Delete Account", id='delete-{}'.format(NAME),
                        n_clicks=0, className="btn btn-lg btn-warning btn-block"),
            html.Div(id='dummy-{}'.format(NAME), hidden=True)
        ],
        className="container",
    )


@app.callback(Output(submit_id, 'children'),
              [],
              [
                  State(biography_id, 'value'),
                  State(email_id, 'value'),
              ],
              [
                  Event(submit_id, 'click')
              ])
def set_mentor_tags(bio: str, email: str):
    """
    Callback that gets called when a tag is added or deleted

    :param bio: Biography of the users.
    :param email: User email address.
    """
    log.info("User %s set bio: %s", current_username(), bio)
    log.info("User %s set email: %s", current_username(), email)
    user = current_user()
    user.bio = bio
    user.email = email
    user.commit()

    return "Saved!"
