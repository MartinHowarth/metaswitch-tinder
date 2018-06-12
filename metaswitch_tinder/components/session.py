import logging
from collections import namedtuple
from typing import List, Optional

import flask

from metaswitch_tinder.database import User, get_user
from .utils import wait_for

log = logging.getLogger(__name__)

SignupInformation = namedtuple(
    "SignupInformation",
    [
        "biography",
        "request_categories",
        "request_details",
        "mentor_categories",
        "mentor_details",
    ],
)


def current_user_email() -> str:
    user_email = flask.session.get("user_email", None)
    if user_email is None:
        raise AssertionError("Could not get current user as they are not logged in.")
    return user_email


def get_current_user() -> User:
    user_email = current_user_email()

    user = get_user(user_email)
    if user is None:
        raise AssertionError(
            "Could not get current user from database by name: %s" % user_email
        )
    return user


def set_current_user_email(email: str):
    flask.session["user_email"] = email


def login(email: str):
    set_current_user_email(email)
    log.info("%s has logged in.", email)


def logout():
    log.info("Logout: %s", flask.session)
    keys = list(flask.session.keys())
    for key in keys:
        del flask.session[key]


def is_logged_in() -> bool:
    log.debug("is_logged_in: Flask session is: %s", flask.session)
    return "user_email" in flask.session


def set_post_login_redirect(href: str):
    log.info("Set post login redirect to: %s", href)
    flask.session["signin_redirect"] = href


def store_signup_information(
    biography: str,
    request_categories: List[str] = None,
    request_details: str = None,
    mentor_categories: List[str] = None,
    mentor_details: str = None,
):
    info = SignupInformation(
        biography,
        request_categories,
        request_details,
        mentor_categories,
        mentor_details,
    )
    flask.session["signup_info"] = info._asdict()


def get_signup_information() -> Optional[SignupInformation]:
    raw_info = flask.session.get("signup_info")
    if raw_info is not None:
        return SignupInformation(**raw_info)
    return None


def clear_signup_information():
    if "signup_info" in flask.session:
        del flask.session["signup_info"]


def wait_for_login():
    wait_for(is_logged_in, 2)


def on_mentee_tab() -> bool:
    return flask.session.get("on_mentee_tab") is True


def set_on_mentee_tab(status: bool):
    flask.session["on_mentee_tab"] = status


def get_last_tab_on(page: str) -> Optional[str]:
    cached_tab = flask.session.get("tab-{}".format(page), None)
    log.debug("%s - Cached tab was: %s", page, cached_tab)
    return cached_tab


def set_last_tab_on(page: str, last_tab: str):
    log.debug("%s - Caching last tab as: %s", page, last_tab)
    flask.session["tab-{}".format(page)] = last_tab


def set_current_request(request_id: str):
    log.debug("User %s storing current request: %s", current_user_email(), request_id)
    flask.session["current_request"] = request_id


def get_current_request() -> str:
    return flask.session["current_request"]
