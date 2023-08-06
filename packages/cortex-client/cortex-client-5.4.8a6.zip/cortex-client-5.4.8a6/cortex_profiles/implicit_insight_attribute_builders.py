from typing import List

import pandas as pd
from cortex_profiles import attribute_builder_utils
from cortex_profiles import implicit_attribute_builder_utils
from cortex_profiles.schemas.dataframes import COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL, \
    TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL, INSIGHT_COLS, INTERACTIONS_COLS
from cortex_profiles.schemas.schemas import CONTEXTS, VERSION
from cortex_profiles.types.attribute_values import CounterAttributeContent, TotalAttributeContent
from cortex_profiles.types.attributes import ObservedProfileAttribute


def derive_counter_attributes_for_count_of_specific_insight_interactions_per_insight_type(interactions_df:pd.DataFrame, insights_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:
    insight_interactions_df = implicit_attribute_builder_utils.derive_count_of_insights_per_interactionType_per_insightType_per_profile(interactions_df, insights_df)
    return attribute_builder_utils.derive_simple_observed_attributes_from_df(
        insight_interactions_df,
        [
            INTERACTIONS_COLS.PROFILEID,
            INSIGHT_COLS.INSIGHTTYPE,
            INTERACTIONS_COLS.INTERACTIONTYPE
        ],
        "countOf"
            + ".insights[{"+COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INSIGHTTYPE+"}]"
            + ".interactedWith[{"+INTERACTIONS_COLS.INTERACTIONTYPE+"}]"
            + ".withinTimeframe["+df_timeframe+"]",
        "total",
        CounterAttributeContent
    )


def derive_dimensional_attributes_for_count_of_specific_insight_interactions_per_encountered_tag(interactions_df:pd.DataFrame, insights_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:
    tag_specific_interactions_df = implicit_attribute_builder_utils.derive_count_of_insights_per_interactionType_per_relatedConcepts_per_profile(interactions_df, insights_df)
    if tag_specific_interactions_df .empty:
        return []
    return attribute_builder_utils.derive_dimensional_observed_attributes_from_df(
        tag_specific_interactions_df[
            tag_specific_interactions_df[COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP] == CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP
            ],
        [
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.PROFILEID, COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INSIGHTTYPE,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE, COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE,
            COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTITLE
        ],
        "countOf"
            + ".insights[{"+COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INSIGHTTYPE+"}]"
            + ".interactedWith[{"+COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE+"}]"
            + ".withinTimeframe[" + df_timeframe + "]"
            + ".relatedToConcept[{"+COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTITLE+"}]",
        COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTID,
        COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TOTAL,
        COUNT_OF_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE,
        CounterAttributeContent
    )


def derive_dimensional_attributes_for_total_duration_of_specific_insight_interactions_per_encountered_tag(interactions_df:pd.DataFrame, insights_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:
    tag_specific_interactions_with_times_df = implicit_attribute_builder_utils.derive_time_spent_on_insights_with_relatedConcepts(
        implicit_attribute_builder_utils.prepare_interactions_per_tag_with_times(interactions_df, insights_df)
    )
    if tag_specific_interactions_with_times_df.empty:
        return []
    return attribute_builder_utils.derive_dimensional_observed_attributes_from_df(
        tag_specific_interactions_with_times_df[
            tag_specific_interactions_with_times_df[TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTRELATIONSHIP] == CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP
            ],
        [
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.PROFILEID,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.INSIGHTTYPE,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE,
            TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTITLE
        ],
        "totalDuration"
            + ".insights[{"+TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.INSIGHTTYPE+"}]"
            + ".interactedWith[{" + TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.INTERACTIONTYPE + "}]"
            + ".withinTimeframe["+df_timeframe+"]"
            + ".relatedToConcept[{"+TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTITLE+"}]",
        TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTID,
        TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TOTAL,
        TIMES_SPENT_ON_TAG_SPECIFIC_INTERACTIONS_COL.TAGGEDCONCEPTTYPE,
        TotalAttributeContent
    )

