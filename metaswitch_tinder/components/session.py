import logging

from flask import session as flask_session
from typing import Optional

from .utils import wait_for
from metaswitch_tinder.database.manage import get_user, User


log = logging.getLogger(__name__)


def current_username() -> Optional[str]:
    return flask_session.get('username', None)


def current_user() -> User:
    return get_user(current_username())


def set_current_usename(username: str):
    flask_session['username'] = username


def login(username: str):
    set_current_usename(username)
    log.info("%s has logged in.", username)


def logout():
    log.info("Logout: %s", flask_session)
    keys = list(flask_session.keys())
    for key in keys:
        del flask_session[key]


def is_logged_in() -> bool:
    return 'username' in flask_session


def wait_for_login():
    wait_for(is_logged_in, 2)


def on_mentee_tab() -> bool:
    return flask_session.get('on_mentee_tab') is True


def set_on_mentee_tab(status: bool):
    flask_session['on_mentee_tab'] = status


def get_last_tab_on(page: str) -> Optional[str]:
    cached_tab = flask_session.get('tab-{}'.format(page), None)
    log.debug("%s - Cached tab was: %s", page, cached_tab)
    return cached_tab


def set_last_tab_on(page: str, last_tab: str):
    log.info("%s - Caching last tab as: %s", page, last_tab)
    flask_session['tab-{}'.format(page)] = last_tab
