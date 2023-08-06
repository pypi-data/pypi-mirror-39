from typing import Dict, List
from operator import or_
from functools import reduce
from django.db.models import Q


def Q_any(key_list_maps: Dict[str, List]):
    return reduce(
        or_,
        (
            Q(**{key: value})
            for key in key_list_maps.keys()
            for value in key_list_maps[key]
        ),
        Q())
