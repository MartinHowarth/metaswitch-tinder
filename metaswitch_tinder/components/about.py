import logging
from typing import List

import dash_html_components as html
from dash.dependencies import Event, Output

from metaswitch_tinder.app import app

log = logging.getLogger(__name__)

NAME = __name__.replace(".", "_")

about_id = f"about-{NAME}"
about_btn_id = f"about-btn-{NAME}"


def about_div() -> html.Div:
    return html.Div([about_button()], id=about_id)


def about_button():
    return html.Button(
        "What's this about?", id=about_btn_id, className="btn btn-warning"
    )


def about_text() -> List:
    return [
        html.P(
            "Metaswitch tinder seeks to create partnerships between people so "
            "they can help each other."
        ),
        html.P(
            "These partnerships can be anything, for example: "
            "a single code review; an ongoing mentorship or a sports partner."
        ),
        html.Br(),
        html.Br(),
        html.H2("Mentees"),
        html.P(
            "Mentees make requests for things they want to learn, or get help about."
        ),
        html.P("Mentees may then choose which mentor they would like."),
        html.P(
            "Until a mentee has chosen a mentor, the mentors cannot see the mentees."
        ),
        html.Br(),
        html.Br(),
        html.H2("Mentors"),
        html.P(
            "Mentors claim to have skills, which is used by this service to match them "
            "to possible mentees."
        ),
        html.P(
            "Mentors will be immediately visible to mentees, once a request has been "
            "made that match your skills."
        ),
        html.P("Once a mentee has accepted you, you may then accept (or reject) them."),
        html.Br(),
        html.Br(),
        html.H2("Matching"),
        html.P(
            "Possible matches are currently generated solely by an "
            "overlap of the tags of mentors and mentee requests."
        ),
        html.P(
            "Once a match is accepted by both parties, an email will be sent to "
            "notify users of the match."
        ),
    ]


@app.callback(Output(about_id, "children"), [], [], [Event(about_btn_id, "click")])
def handle_about_button_click():
    """
    Handles the user clicking the about button.

    Return value of this sets the children fo the about div.
    """
    return about_text()
