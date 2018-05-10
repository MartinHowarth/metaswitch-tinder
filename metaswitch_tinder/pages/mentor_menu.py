from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.components.tabs import generate_tabs


def mentor_menu(config: MetaswitchTinder):
    return generate_tabs({'Messages': 'messages', 'Matches': 'matches'}, 'matches')