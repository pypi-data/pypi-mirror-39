import copy
from typing import List

from attr import attrs, Factory, attrib, validators
from cortex_profiles.schemas.schemas import CONTEXTS, VERSION
from cortex_profiles.types.attribute_values import BaseAttributeValue
from cortex_profiles.types.utils import load_profile_attribute_value_from_dict
from cortex_profiles.utils import utc_timestamp, unique_id, converter_for_classes


@attrs(frozen=True)
class ProfileAttribute(object):
    id = attrib(type=str) # What is the id of this piece of data?
    context = attrib(type=str)  # What is the type of the data being captured by this data type?
    version = attrib(type=str) # What version of the data type is being adhered to?
    profileId = attrib(type=str)  # Who is this attribute applicable to?
    profileType = attrib(type=str)  # What kind of entity is represented by this profile?
    createdAt = attrib(type=str)  # When was this attribute created?
    attributeKey = attrib(type=str)  # What is the id of the attribute?
    attributeValue = attrib(
        type=BaseAttributeValue,
        validator=[validators.instance_of(BaseAttributeValue)],
        converter=lambda x: converter_for_classes(x, BaseAttributeValue, dict_constructor=load_profile_attribute_value_from_dict)
    )  # What value is associated with the profile attribute?
    tenantId = attrib(type=str, default=None)
    environmentId = attrib(type=str, default=None)
    onLatestProfile = attrib(type=bool, default=True)  # Is this attribute on the latest profile?
    commits = attrib(type=List[str], factory=list)  # What commits is this attribute associated with?


@attrs(frozen=True, auto_attribs=True)
class InferredProfileAttribute(ProfileAttribute):
    inferredAt: str = Factory(utc_timestamp) # When was this attribute inferred at?
    inferred: bool = True  # Was this attribute inferred?
    id: str = Factory(unique_id)
    context: str = CONTEXTS.INFERRED_PROFILE_ATTRIBUTE
    version: str = VERSION


@attrs(frozen=True, auto_attribs=True)
class ObservedProfileAttribute(ProfileAttribute):
    observedAt: str = Factory(utc_timestamp) # When was this attribute observed at?
    observed: bool = True  # Was this attribute observed?
    id: str = Factory(unique_id)
    context: str = CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE
    version: str = VERSION


@attrs(frozen=True, auto_attribs=True)
class DeclaredProfileAttribute(ProfileAttribute):
    declaredAt: str = Factory(utc_timestamp) # When did the user declare this attribute about themselves?
    declared: bool = True  # Was this profile attribute declared by the user?
    id: str = Factory(unique_id)
    context: str = CONTEXTS.DECLARED_PROFILE_ATTRIBUTE
    version: str = VERSION


# ProfileAttribute = Union[InferredProfileAttribute, DeclaredProfileAttribute, ObservedProfileAttribute]
# ProfileAttributeKinds = Union[
#     PercentageAttributeContent,
#     CounterAttributeContent,
#     DimensionalAttributeContent,
#     MultiDimensionalAttributeContent
# ]


def load_profile_attribute_from_dict(d: dict) -> ProfileAttribute:
    # updated_dict["attributeValue"] = load_profile_attribute_value_from_dict(updated_dict["attributeValue"])
    updated_dict = copy.deepcopy(d)
    # Deep Copy works as expected with Nones :: copy.deepcopy({"a": {"b": None}}) => Out[18]: {'a': {'b': None}}
    # print("Normal dict ", d)
    # print("Updated dict ", updated_dict)
    if d.get("context") == CONTEXTS.INFERRED_PROFILE_ATTRIBUTE:
        return InferredProfileAttribute(**updated_dict)
    if d.get("context") == CONTEXTS.OBSERVED_PROFILE_ATTRIBUTE:
        return ObservedProfileAttribute(**updated_dict)
    if d.get("context") == CONTEXTS.DECLARED_PROFILE_ATTRIBUTE:
        return DeclaredProfileAttribute(**updated_dict)
    return None