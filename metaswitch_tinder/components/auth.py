import flask
import logging
import os

from dash.dependencies import Output, Event

from metaswitch_tinder.app import app, OAUTH_REDIRECT_URI, google
from metaswitch_tinder.app_structure import href
from metaswitch_tinder.components import session
from metaswitch_tinder.database.models import username_already_exists, handle_signup_submit, create_request


log = logging.getLogger(__name__)

NAME = __name__.replace('.', '_')


debug_login_target = 'debug_login_target'


def authenticated_login_is_enabled() -> bool:
    if 'GOOGLE_ID' in os.environ:
        return True
    return False


def handle_login(username: str, email: str):
    log.info("Handling login for: %s, %s", username, email)

    # If the user logged in (or signed up) as part of submitting information, then we will have stored that information.
    signup_info = session.get_signup_information()

    if username_already_exists(username):
        # User already exists - handle the login and make a request if necessary.
        log.debug("User %s has already signed up.", username)

        session.login(username)

        # If we stored request info, then make a request according to that.
        if signup_info and signup_info.request_categories:
            create_request(username, signup_info.request_categories, signup_info.request_details)

    elif signup_info:
        log.debug("User %s has signed up with additional information: %s", username, signup_info)
        # Create the user with whatever information was given.
        handle_signup_submit(username, email, signup_info.biography,
                             signup_info.mentor_categories, signup_info.mentor_details)

        # If the user made a request as part of login, then make a request according to that.
        if signup_info.request_categories:
            create_request(username, signup_info.request_categories, signup_info.request_details)
    else:
        log.debug("User %s has signed up with no additional information.", username)
        # If the user just signed up without additional information, just create them.
        handle_signup_submit(username, email)

    session.clear_signup_information()
    session.login(username)


@app.server.route(OAUTH_REDIRECT_URI)
def authorized_by_google():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            flask.request.args['error_reason'],
            flask.request.args['error_description']
        )
    flask.session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo').data

    log.debug("User data from google is: %s" % user_info)
    username = user_info['name']
    email = user_info['email']

    handle_login(username, email)

    redirect_href = flask.session.get('signin_redirect', '/')
    log.debug("Google login completed, redirecting to: %s", redirect_href)
    return flask.redirect(redirect_href)


if authenticated_login_is_enabled():
    @google.tokengetter
    def get_access_token():
        return flask.session.get('google_token')


@app.server.route('/login')
def login():
    if session.is_logged_in():
        redirect_target = flask.session.get('signin_redirect', '/')
    elif 'GOOGLE_ID' in os.environ:
        redirect_target = flask.url_for('login_with_google')
    else:
        redirect_target = href(__name__, debug_login_target)
    return flask.redirect(redirect_target)


@app.server.route('/login-with-google')
def login_with_google():
    callback = flask.url_for('authorized_by_google', _external=True)
    return google.authorize(callback=callback)


@app.callback(
    Output('logout', ''),
    [],
    [],
    [Event('logout', 'click')]
)
def handle_logout():
    session.logout()


def layout():
    """Required to use the app_structure, even though this isn't a page of its own."""
    return
