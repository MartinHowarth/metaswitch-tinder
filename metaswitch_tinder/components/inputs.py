from typing import List

import dash_core_components as dcc


def multi_dropdown_with_tags(
    tags: List[str], _id: str, init_selection: List[str] = None
):
    tag_list = [{"label": tag, "value": tag} for tag in tags]

    return dcc.Dropdown(
        options=tag_list, value=init_selection or [], multi=True, id=_id
    )
