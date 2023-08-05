from typing import List, Optional

from attr import attrs, Factory

from cortex_profiles.schemas.schemas import CONTEXTS, VERSION
from cortex_profiles.types.attributes import ProfileAttribute, load_profile_attribute_from_dict
from cortex_profiles.types.utils import get_types_of_union
from cortex_profiles.utils import merge_dicts


@attrs(frozen=True, auto_attribs=True)
class ProfileAttributeMapping(object):
    attributeKey: str # What is the name of the attribute in the profile?
    attributeId: str # What is the id for the attribute in the profile?


@attrs(frozen=True, auto_attribs=True)
class Profile(object):
    id: str  # What is the id of this piece of data? aka snapshotId
    createdAt: str # When was this snapshot created?
    tenantId: str # Which tenant does this attribute belong in?
    environmentId: str # Which environment does this profile live in?
    commitId: str  # Which commit is this linked based off of?
    version: str = VERSION  # What version of the system does this piece of data adhere to?
    context: str = CONTEXTS.PROFILE  # What is the type of the data being captured by this data type?
    attributes: List[ProfileAttributeMapping] = Factory(list)  # Which attributes exist in this snapshot?

    @staticmethod
    def from_dict(d:dict):
        mapped_attributes = [] if not d.get("attributes") else d["attributes"]
        mapped_attributes = [
            ProfileAttributeMapping(**attribute) if not isinstance(attribute, ProfileAttributeMapping) else attribute
            for attribute in mapped_attributes
        ]
        return Profile(
            **merge_dicts(d, {
                "attributes": mapped_attributes
            })
        )


@attrs(frozen=True, auto_attribs=True)
class ProfileSnapshot(object):
    id: str  # What is the id of this piece of data? aka snapshotId
    createdAt: str # When was this snapshot created?
    tenantId: str # Which tenant does this attribute belong in?
    environmentId: str # Which environment does this profile live in?
    commitId: str  # Which commit was responsible for creating this updated profile?
    version: str = VERSION  # What version of the system does this piece of data adhere to?
    context: str = CONTEXTS.PROFILE  # What is the type of the data being captured by this data type?
    attributes: List[ProfileAttribute] = Factory(list)  # Which attributes exist in this snapshot?

    @staticmethod
    def from_dict(d:dict):
        mapped_attributes = [] if not d.get("attributes") else d["attributes"]
        mapped_attributes = [
            load_profile_attribute_from_dict(attribute) if not isinstance(attribute, get_types_of_union(ProfileAttribute)) else attribute
            for attribute in mapped_attributes
        ]
        return Profile(
            **merge_dicts(d, {
                "attributes": mapped_attributes
            })
        )


@attrs(frozen=True, auto_attribs=True)
class ProfileCommit(object):
    id: str  # What is the id of this piece of data? aka commitId
    createdAt: str  # When was this snapshot created?
    tenantId: str  # Which tenant does this attribute belong in?
    environmentId: str  # Which environment does this profile live in?
    profileId: str  # What profile is this commit on?
    extends: Optional[str] = None  # What is the id of the commit this commit extends?
    attributesModified: Optional[List[ProfileAttributeMapping]] = Factory(list)  # Which attributes were modified in the commit?
    attributesAdded: Optional[List[ProfileAttributeMapping]] = Factory(list)  # Which attributes were added ?
    attributesRemoved: Optional[List[ProfileAttributeMapping]] = Factory(list)  # Which attributes were removed in the commit?
    version: str = VERSION  # What version of the system does this piece of data adhere to?
    context: str = CONTEXTS.PROFILE_COMMIT  # What is the type of the data being captured by this data type?


