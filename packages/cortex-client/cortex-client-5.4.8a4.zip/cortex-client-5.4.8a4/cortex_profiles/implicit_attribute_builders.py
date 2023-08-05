from typing import List

import pandas as pd
from cortex_profiles import utils
from cortex_profiles import implicit_login_attribute_builders, implicit_insight_attribute_builders
from cortex_profiles.types.attributes import ProfileAttribute


def derive_attributes_from_timeranged_dataframes(timerange:str, insights_df: pd.DataFrame, interactions_df: pd.DataFrame, sessions_df: pd.DataFrame) -> List[ProfileAttribute]:
    return utils.flatten_list_recursively([
        implicit_insight_attribute_builders.derive_counter_attributes_for_count_of_specific_insight_interactions_per_insight_type(
            interactions_df, insights_df, timerange),
        implicit_insight_attribute_builders.derive_dimensional_attributes_for_count_of_specific_insight_interactions_per_encountered_tag(
            interactions_df, insights_df, timerange),
        implicit_insight_attribute_builders.derive_dimensional_attributes_for_total_duration_of_specific_insight_interactions_per_encountered_tag(
            interactions_df, insights_df, timerange),
        implicit_login_attribute_builders.derive_counter_attributes_for_specific_logins(sessions_df, timerange),
        implicit_login_attribute_builders.derive_counter_attributes_for_login_durations(sessions_df, timerange),
        implicit_login_attribute_builders.derive_dimensional_attributes_for_daily_login_counts(sessions_df, timerange),
        implicit_login_attribute_builders.derive_dimensional_attributes_for_daily_login_durations(sessions_df, timerange),
        implicit_login_attribute_builders.derive_average_attributes_for_daily_login_counts(sessions_df, timerange),
        implicit_login_attribute_builders.derive_average_attributes_for_daily_login_duration(sessions_df, timerange)
    ])

