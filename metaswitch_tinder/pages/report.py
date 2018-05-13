import dash_core_components as dcc
import dash_html_components as html
import logging

from dash.dependencies import Output, State, Event

from metaswitch_tinder import tinder_email
from metaswitch_tinder.app import app
from metaswitch_tinder.app_structure import href


log = logging.getLogger(__name__)


NAME = __name__.replace('.', '')

submit = "submit"


def layout():
    return html.Div([
        html.H1("Report an issue", className="text-center"),
        html.Br(),
        dcc.Textarea(placeholder='Report an issue or inappropriate content.  '
                                 'Please include as much information as possible',
                     value='', id='report-{}'.format(NAME),
                     style={'width': '100%'}),
        dcc.Link(html.Button("Submit Report", id='submit-{}'.format(NAME),
                             n_clicks=0, className="btn btn-sm btn-danger btn-block"),
                 href=href(__name__, submit))
    ], className="container text-center")


@app.callback(
    Output('report', ''),
    [],
    [
        State('report-{}'.format(NAME), 'value'),
    ],
    [Event('submit-{}'.format(NAME), 'click')]
)
def report_email(report_text):
    log.info("Report submitted with text: %s", report_text)
    tinder_email.send_report_email(report_text)


def report_button():
    return dcc.Link("Report", href=href(__name__), className="btn btn-primary btn-block btn-danger", id='report')
