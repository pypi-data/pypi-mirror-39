from cortex_profiles.types.general import dotdict

COMMIT_COL = dotdict(dict(
    COMMIT_ID="commitId",
    TIMESTAMP="timestamp",
    ATTRS_ADDED="attributesAdded",
    ATTRS_REMOVED="attributesRemoved",
    ATTRS_MODIFIED="attributesModified",
))


ATTRIBUTE_COL = dotdict(dict(
    ATTRIBUTE_KEY="attributeKey",
    ATTRIBUTE_ID="attributeId",
    ATTRIBUTE_TYPE="attributeType",
    ATTRIBUTE_VALUE_TYPE="attributeValueType",
))


PROFILE_COL = dotdict(dict(
    PROFILE_ID="profileId",
    PROFILE_TYPE="profileType",
))