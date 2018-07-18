from typing import List

import dash_html_components as html

from melinda.components.session import (
    current_user_email,
    get_current_user,
    is_logged_in,
)
from melinda.database import Request, get_user


def children_no_matches():
    return [
        html.H1("{}, you have no completed matches! :(".format(current_user_email()))
    ]


def children_matches(completed_matches: List[Request]) -> List:
    table_rows = [
        html.Tr(
            [
                html.Td("Partner"),
                html.Td("Request tags"),
                html.Td("Request description"),
            ],
            className="table-active",
        )
    ]

    for match in completed_matches:
        if match.maker == current_user_email():
            # Current user is the mentee
            other_user = get_user(match.mentor)
            name = other_user.name if other_user else "unknown"
            partner_name = "{} (mentor)".format(name)
        else:
            # Current user is the mentor
            other_user = get_user(match.maker)
            name = other_user.name if other_user else "unknown"
            partner_name = "{} (mentee)".format(name)

        table_rows.append(
            html.Tr(
                [
                    html.Td(partner_name),
                    html.Td(", ".join(match.tags)),
                    html.Td(match.comment),
                ],
                className="table-light",
            )
        )
    return [
        html.H1("{}, here are your completed matches".format(get_current_user().name)),
        html.Table([*table_rows], className="table table-condensed"),
    ]


def layout():
    if is_logged_in():
        user = get_current_user()
    else:
        return html.Div([html.Br(), html.H1("You must be logged in to do this")])

    completed_matches = user.get_matches()  # type: List[Request]

    if not completed_matches:
        children = children_no_matches()
    else:
        children = children_matches(completed_matches)

    return html.Div(children=children, className="container")
