# -*- coding: utf-8 -*-
import logging
import os
import sys

import dash
import dash_core_components as dcc
import dash_html_components as html
import flask

import melinda.pages.report
from melinda import app_globals, app_structure
from melinda.app import app
from melinda.app_config import config
from melinda.app_globals import JAVASCRIPT_DIR
from melinda.components import widgets

log = logging.getLogger(__name__)


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    ch.setFormatter(formatter)
    root.addHandler(ch)


configure_logging()

app.css.append_css({"external_url": config.css_cdn})

app_structure.generate_structure()

# Main app layout
app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        html.Div(
            [
                html.Div(widgets.logout_button()),
                html.Div(melinda.pages.report.report_button()),
            ],
            className="d-flex flex-row justify-content-between",
        ),
        # The 'page-content' is where all content appears
        html.Div(id="page-content"),
    ]
)


@app.callback(
    dash.dependencies.Output("page-content", "children"),
    [dash.dependencies.Input("url", "pathname")],
)
def display_page(pathname: str):
    """
    Callback that gets called when the url changes.

    It is used to determine what html to display for the new url.
    :param pathname: URL including the first `/` but excluding the domain.
        I.e. "http://my-app.com/page-1" would be passed in here as "/page-1"
    :return: Dash html object to display as the children of the 'page-content'
        Div in the main layout.
    """
    if app_globals.structure is None:
        raise RuntimeError("`generate_structure` has not been called.")

    return {
        href: getattr(details["module"], "layout")
        for href, details in app_globals.structure.items()
    }.get(pathname, lambda: "404: Not found!")()


# Add each script to the app from the JAVASCRIPT_DIR
for script in os.listdir(JAVASCRIPT_DIR):
    if os.path.splitext(script)[1] != ".js":
        continue
    app.scripts.append_script({"external_url": "/static/{}".format(script)})


# Use Flask to serve the javascript source files statically.
@app.server.route("/static/<filename>.js")
def serve_script(filename):
    return flask.send_from_directory(JAVASCRIPT_DIR, "{}.js".format(filename))


if __name__ == "__main__":
    if "DATABASE_URL" not in os.environ:
        # Populate the in-memory test database.
        from melinda import review_app_database

        review_app_database.populate()
        os.environ["NO_EMAIL"] = "true"

    app.run_server(port=int(os.environ.get("PORT", 80)), debug=True, threaded=True)
else:
    # The `server` is imported here so that gunicorn's entry point is this file.
    # That forces load of all the layouts and callbacks in this file.
    from melinda.app import server  # noqa
