from typing import List

import dash_core_components as dcc

from metaswitch_tinder.database.models import Tag


def multi_dropdown_with_tags(
    tags: List[Tag], _id: str, init_selection: List[str] = None
):
    tag_list = [{"label": tag.name, "value": tag.name} for tag in tags]

    return dcc.Dropdown(
        options=tag_list, value=init_selection or [], multi=True, id=_id
    )
