from typing import Optional, List

from attr import attrs
from cortex_profiles.schemas.schemas import VERSION


@attrs(frozen=True, auto_attribs=True)
class Link(object):
    context: str  # What is the type of the data being captured by this data type?
    id: str  # What is the id of this piece of data?
    title: Optional[str] = None # What is the human friendly name of this link?
    version: str = VERSION  # What version of the data type is being adhered to?


@attrs(frozen=True, auto_attribs=True)
class InsightTag(object):
    context: str  # What is the type of the data being captured by this data type?
    id: str  # What is the id of this piece of data?
    insight: Link # What insight is this tag about?
    concept: Link # What concept is being tagged by the insight?
    relationship: Link # What relationship does the tagged concept have with regards to the insight?


@attrs(frozen=True, auto_attribs=True)
class Insight(object):
    context: str  # What is the type of the data being captured by this data type?
    id: str  # What is the id of this piece of data?
    insightType: str # What kind of insight is this?
    profileId: str # What profile was this insight generated for?
    dateGeneratedUTCISO: str # When was this insight generated?
    appId: str # Which app was this insight generated for?
    tags: List # What concepts were tagged in this insight?


@attrs(frozen=True, auto_attribs=True)
class InsightRelatedToConceptTag(object):
    """
    Representing how an insight relates to other concepts ...
    """
    version: str  # What version of the data type is being adhered to?
    context: str  # What is the type of the data being captured by this data type?
    id: str  # What is the id of this piece of data?
    insight: Link # What insight is this relationship about?
    concept: Link # What concept is the insight related to?


