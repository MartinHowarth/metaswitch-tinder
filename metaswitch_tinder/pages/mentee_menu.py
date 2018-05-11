from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.components.tabs import generate_tabs


def mentee_menu():
    return generate_tabs({'Messages': 'messages', 'Matches': 'matches'}, 'matches')
