import logging
import os

import dash
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

from metaswitch_tinder.app_config import config

log = logging.getLogger(__name__)

app = dash.Dash()
app.title = config.app_name

# Since we're adding callbacks to elements that don't exist in the app.layout,
# Dash will raise an exception to warn us that we might be
# doing something wrong.
# In this case, we're adding the elements through a callback, so we can ignore
# the exception.
app.config.suppress_callback_exceptions = True

server = app.server
server.secret_key = os.environ.get("SECRET_KEY", "secret")
server.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///:memory:"
)
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config["GOOGLE_ID"] = os.environ.get("GOOGLE_ID")
server.config["GOOGLE_SECRET"] = os.environ.get("GOOGLE_SECRET")

OAUTH_REDIRECT_URI = "/oauth2_callback"
oauth = OAuth(app.server)

if "GOOGLE_ID" in os.environ:
    google = oauth.remote_app(
        "google",
        request_token_params={"scope": "email"},
        base_url="https://www.googleapis.com/oauth2/v1/",
        request_token_url=None,
        access_token_method="POST",
        access_token_url="https://accounts.google.com/o/oauth2/token",
        authorize_url="https://accounts.google.com/o/oauth2/auth",
        consumer_key=app.server.config.get("GOOGLE_ID"),
        consumer_secret=app.server.config.get("GOOGLE_SECRET"),
    )
else:
    google = None

db = SQLAlchemy(server)
