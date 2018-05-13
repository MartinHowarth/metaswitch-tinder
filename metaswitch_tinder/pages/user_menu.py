import logging

from metaswitch_tinder.components.auth import wait_for_login
from metaswitch_tinder.components.tabs import generate_tabs


log = logging.getLogger(__name__)


def layout():
    wait_for_login()
    return generate_tabs(
        {
            'Messages': 'messages',
            'Matches': 'matches',
            'Settings': 'settings'
        },
        default_tab='matches'
    )
