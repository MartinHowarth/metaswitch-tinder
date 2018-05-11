from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.components.tabs import generate_tabs
from metaswitch_tinder.database.manage import User, list_all_users, get_user

def mentor_menu(config: MetaswitchTinder):
    return generate_tabs({'Messages': 'messages', 'Matches': 'matches'}, 'matches')
