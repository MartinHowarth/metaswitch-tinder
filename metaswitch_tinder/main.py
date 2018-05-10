# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import importlib
import json
import logging
import os
import sys

from dash.dependencies import Input, Output
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder import pages, tabs, example_config, global_config
from metaswitch_tinder.tinder_email import send_email

log = logging.getLogger(__name__)


def configure_logging():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    ch = logging.StreamHandler(sys.stderr)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)


def load_config_from_file() -> MetaswitchTinder:
    if len(sys.argv) > 1:
        # Strip the .py extension
        config_file = os.path.splitext(sys.argv[1])[0]
        config_module = importlib.import_module(config_file)
        config_dict = config_module.config
    else:
        # Default to example_config
        config_dict = example_config.config

    cfg = MetaswitchTinder(config_dict, partial=False)
    cfg.validate()
    return cfg


def load_config_from_env() -> MetaswitchTinder:
    cfg = MetaswitchTinder(json.loads(os.environ['ALL_CONFIG']), partial=False)
    cfg.validate()
    return cfg


config = MetaswitchTinder(example_config.config, partial=False)
config.validate()

server = Flask(__name__)

server.secret_key = os.environ.get('secret_key', 'secret')
server.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
global_config.DATABASE = SQLAlchemy(server)

app = dash.Dash(name=__name__, server=server)

app.config.suppress_callback_exceptions = True
app.css.append_css({"external_url": config.css_cdn})


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    return pages.pages.get(pathname, pages.home)(config)


@app.callback(dash.dependencies.Output('tab-content', 'children'),
              [dash.dependencies.Input('tabs', 'value')])
def display_tab(value):
    return tabs.tabs[value](config)

if __name__ == "__main__":
    configure_logging()
    app.run_server(threaded=True, port=int(os.environ.get('PORT', 80)), debug=True)
