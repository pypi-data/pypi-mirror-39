from cortex_profiles.types.general import dotdict


INTERACTION_DURATIONS_COLS = dotdict(dict(
    STARTED_INTERACTION="startedInteractionISOUTC",
    STOPPED_INTERACTION="stoppedInteractionISOUTC",
))


INSIGHT_COLS = dotdict(dict(
    CONTEXT="context",
    ID="id",
    APPID="appId",
    TAGS="tags",
    INSIGHTTYPE="insightType",
    PROFILEID="profileId",
    DATEGENERATEDUTCISO="dateGeneratedUTCISO",
))


SESSIONS_COLS = dotdict(dict(
    CONTEXT="context",
    ID="id",
    ISOUTCENDTIME="isoUTCStartTime",
    ISOUTCSTARTTIME= "isoUTCEndTime",
    PROFILEID="profileId",
    APPID="appId",
    DURATIONINSECONDS="durationInSeconds",
))


INTERACTIONS_COLS = dotdict(dict(
    CONTEXT="context",
    ID="id",
    INTERACTIONTYPE="interactionType",
    INSIGHTID="insightId",
    PROFILEID="profileId",
    SESSIONID="sessionId",
    INTERACTIONDATEISOUTC="interactionDateISOUTC",
    PROPERTIES="properties",
    CUSTOM="custom",
))


COUNT_OF_INTERACTIONS_COL = dotdict(dict(
    PROFILEID="profileId",
    INSIGHTTYPE="insightType",
    INTERACTIONTYPE="interactionType",
    TOTAL="total",
))


COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL = dotdict(dict(
    PROFILEID="profileId",
    INSIGHTTYPE="insightType",
    INTERACTIONTYPE="interactionType",
    TAGGEDCONCEPTTYPE="taggedConceptType",
    TAGGEDCONCEPTRELATIONSHIP="taggedConceptRelationship",
    TAGGEDCONCEPTID="taggedConceptId",
    TAGGEDCONCEPTTITLE="taggedConceptTitle",
    TAGGEDON="taggedOn",
    TOTAL="total",
))


TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL = dotdict(dict(
    PROFILEID="profileId",
    INSIGHTTYPE="insightType",
    INTERACTIONTYPE="interactionType",
    TAGGEDCONCEPTTYPE="taggedConceptType",
    TAGGEDCONCEPTRELATIONSHIP="taggedConceptRelationship",
    TAGGEDCONCEPTID="taggedConceptId",
    TAGGEDCONCEPTTITLE="taggedConceptTitle",
    TAGGEDON="taggedOn",
    ISOUTCSTARTTIME=INTERACTION_DURATIONS_COLS.STARTED_INTERACTION,
    ISOUTCENDTIME=INTERACTION_DURATIONS_COLS.STOPPED_INTERACTION,
    TOTAL="duration_in_seconds",
))


INSIGHT_ACTIVITY_COLS = dotdict(dict(
    ACTIVITY_TIME="isoUTCActivityTime",
    APPID=SESSIONS_COLS.APPID,
    PROFILEID=SESSIONS_COLS.PROFILEID,
    ISOUTCSTARTTIME=SESSIONS_COLS.ISOUTCSTARTTIME,
    ISOUTCENDTIME=SESSIONS_COLS.ISOUTCENDTIME,
))


LOGIN_COUNTS_COL = dotdict(dict(
    CONTEXT="context",
    ID="id",
    APPID="appId",
    PROFILEID="profileId",
    TOTAL="total_logins",
))


LOGIN_DURATIONS_COL = dotdict(dict(
    CONTEXT="context",
    ID="id",
    APPID="appId",
    PROFILEID="profileId",
    DURATION=SESSIONS_COLS.DURATIONINSECONDS,
))


DAILY_LOGIN_COUNTS_COL = dotdict(dict(
    CONTEXT="context",
    ID="id",
    APPID="appId",
    PROFILEID="profileId",
    TOTAL="total_logins",
    DAY="day",
))


DAILY_LOGIN_DURATIONS_COL = dotdict(dict(
    CONTEXT="context",
    ID="id",
    APPID="appId",
    PROFILEID="profileId",
    DURATION=SESSIONS_COLS.DURATIONINSECONDS,
    DAY="day",
))
