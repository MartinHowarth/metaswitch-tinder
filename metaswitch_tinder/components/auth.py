import flask

from dash.dependencies import Output, Event

from metaswitch_tinder.app import app, OAUTH_REDIRECT_URI, google, log
from metaswitch_tinder.components import session
from metaswitch_tinder.database.models import username_already_exists, handle_signup_submit, create_request


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

    # If the user logged in (or signed up) as part of submitting information, then we will have stored that information.
    signup_info = session.get_signup_information()

    if username_already_exists(username):
        # User already exists - handle the login and make a request if necessary.
        # Do not update bio/mentor details even if they were given.
        session.login(username)

        # If we stored request info, then make a request according to that.
        if signup_info and signup_info.request_categories:
            create_request(username, signup_info.request_categories, signup_info.request_details)

    elif signup_info:
        # Create the user with whatever information was given.
        handle_signup_submit(username, email, signup_info.biography,
                             signup_info.mentor_categories, signup_info.mentor_details)

        # If the user made a request as part of login, then make a request according to that.
        if signup_info.request_categories:
            create_request(username, signup_info.request_categories, signup_info.request_details)
    else:
        # If the user just signed up without additional information, just create them.
        handle_signup_submit(username, email)

    session.clear_signup_information()
    session.login(username)

    redirect_href = flask.session.get('signin_redirect', '/')
    log.info("Login completed, redirecting to: %s", redirect_href)
    return flask.redirect(redirect_href)


@google.tokengetter
def get_access_token():
    return flask.session.get('google_token')


@app.server.route('/login-with-google')
def login():
    if session.is_logged_in():
        return flask.redirect(flask.session.get('signin_redirect', '/'))
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
