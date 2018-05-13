from flask import session

from .utils import wait_for


def current_username():
    return session.get('username', None)


def set_current_usename(username):
    session['username'] = username


def is_logged_in():
    return 'username' in session


def wait_for_login():
    wait_for(is_logged_in, 2)
