from typing import Tuple

from cortex_profiles.types.attribute_values import *


def get_types_of_union(union:Union) -> Tuple[type]:
    return union.__args__