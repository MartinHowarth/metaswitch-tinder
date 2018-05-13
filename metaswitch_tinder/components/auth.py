from flask import session

from .utils import wait_for
from metaswitch_tinder.database.manage import get_user, User


def current_username() -> str:
    return session.get('username', None)


def current_user() -> User:
    return get_user(current_username())


def set_current_usename(username: str):
    session['username'] = username


def is_logged_in() -> bool:
    return 'username' in session


def wait_for_login():
    wait_for(is_logged_in, 2)
