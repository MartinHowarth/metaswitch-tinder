from metaswitch_tinder.config_model import MetaswitchTinder
from metaswitch_tinder.components.tabs import generate_tabs
from metaswitch_tinder.database.manage import User, list_all_users, get_user, Request, get_request_by_user, delete_table, purge_table
def mentor_menu(config: MetaswitchTinder):
    return generate_tabs({'Messages': 'messages', 'Matches': 'matches'}, 'matches')

x = Request("Henry", ["sip", "rtp"], "I want lern stuff", "unmatched")

purge_table(Request)

x.add()

hits = get_request_by_user("Henry")

for x in hits:
    print(x)

