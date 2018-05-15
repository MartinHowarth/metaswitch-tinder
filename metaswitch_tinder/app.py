import dash
import os

from flask_sqlalchemy import SQLAlchemy

from metaswitch_tinder.app_config import config

app = dash.Dash()
app.title = config.app_name

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

server = app.server
server.secret_key = os.environ.get('SECRET_KEY', 'secret')
server.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///:memory:')
server.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(server)
