import logging

import dash_core_components as dcc
import dash_html_components as html

from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components.grid import create_equal_row

log = logging.getLogger(__name__)

im_a_mentee = "im_a_mentee"
im_a_mentor = "im_a_mentor"


def layout():
    return html.Div(
        [
            html.H1("Metaswitch Tinder", className="cover-heading"),
            html.P(
                "Metaswitch Tinder is a match-making service for informal mentoring "
                "and unofficial pastoral support "
                "at Metaswitch.",
                className="lead",
            ),
            create_equal_row(
                [
                    dcc.Link(
                        "I'm a mentor!",
                        href=href(__name__, im_a_mentor),
                        className="btn btn-lg btn-secondary",
                    ),
                    dcc.Link(
                        "I'm a mentee!",
                        href=href(__name__, im_a_mentee),
                        className="btn btn-lg btn-primary",
                    ),
                ]
            ),
        ],
        className="container text-center",
    )
