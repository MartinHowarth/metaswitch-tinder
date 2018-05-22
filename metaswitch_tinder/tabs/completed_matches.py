import dash_html_components as html

from typing import List


from metaswitch_tinder.database import Request
from metaswitch_tinder.components.session import is_logged_in, get_current_user, current_username


def children_no_matches():
    return [html.H1("{}, you have no completed matches! :(".format(current_username()))]


def children_matches(completed_matches: List[Request]) -> List:

    table_rows = [
        html.Tr([
            html.Td("Partner"),
            html.Td("Request tags"),
            html.Td("Request description")
        ], className="table-active"),
        ]

    for match in completed_matches:
        if match.maker == current_username():
            # Current user is the mentee
            partner_name = "{} (mentor)".format(match.mentor)
        else:
            # Current user is the mentor
            partner_name = "{} (mentee)".format(match.maker)

        table_rows.append(
            html.Tr([
                html.Td(partner_name),
                html.Td(', '.join(match.tags)),
                html.Td(match.comment)
            ], className="table-light")
        )
    return [
        html.H1("{}, here are your completed matches".format(current_username())),
        html.Table([
            *table_rows
        ], className="table table-condensed"),
    ]


def layout():
    if is_logged_in():
        user = get_current_user()
    else:
        return html.Div([html.Br(),
                         html.H1("You must be logged in to do this")])

    completed_matches = user.get_matches()  # type: List[Request]

    if not completed_matches:
        children = children_no_matches()
    else:
        children = children_matches(completed_matches)

    return html.Div(
        children=children,
        className="container",
    )
