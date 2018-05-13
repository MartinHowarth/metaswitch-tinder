from flask import session as flask_session

from .utils import wait_for
from metaswitch_tinder.database.manage import get_user, User


def current_username() -> str:
    return flask_session.get('username', None)


def current_user() -> User:
    return get_user(current_username())


def set_current_usename(username: str):
    flask_session['username'] = username


def is_logged_in() -> bool:
    return 'username' in flask_session


def wait_for_login():
    wait_for(is_logged_in, 2)


def on_mentee_tab() -> bool:
    return flask_session.get('on_mentee_tab') is True


def set_on_mentee_tab(status: bool):
    flask_session['on_mentee_tab'] = status
