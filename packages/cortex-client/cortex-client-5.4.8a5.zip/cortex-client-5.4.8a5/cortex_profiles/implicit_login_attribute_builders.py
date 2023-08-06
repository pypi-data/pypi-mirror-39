"""
Users dont really configure how these attributes are derived ... they just are ...
"""

from typing import List

import pandas as pd

from cortex_profiles import attribute_builder_utils, implicit_attribute_builder_utils
from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.schemas.dataframes import LOGIN_COUNTS_COL, LOGIN_DURATIONS_COL, DAILY_LOGIN_DURATIONS_COL, DAILY_LOGIN_COUNTS_COL
from cortex_profiles.types.attributes import ObservedProfileAttribute
from cortex_profiles.types.attribute_values import CounterAttributeContent, TotalAttributeContent, AverageAttributeValue

# - [x] Do all of the sessions based stuff in here ...


def derive_counter_attributes_for_specific_logins(sessions_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:
    login_counts_df = implicit_attribute_builder_utils.derive_count_of_user_logins(sessions_df)
    return attribute_builder_utils.derive_simple_observed_attributes_from_df(
        login_counts_df,
        [
            LOGIN_COUNTS_COL.PROFILEID,
            LOGIN_COUNTS_COL.APPID,
        ],
        "countOf"
            + ".logins[{"+LOGIN_COUNTS_COL.APPID+"}]"
            + ".withinTimeframe["+df_timeframe+"]",
        LOGIN_COUNTS_COL.TOTAL,
        CounterAttributeContent
    )


def derive_counter_attributes_for_login_durations(sessions_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:
    login_durations_df = implicit_attribute_builder_utils.derive_time_users_spent_logged_in(sessions_df)
    return attribute_builder_utils.derive_simple_observed_attributes_from_df(
        login_durations_df,
        [
            LOGIN_DURATIONS_COL.PROFILEID,
            LOGIN_DURATIONS_COL.APPID,
        ],
        "durationOf"
            + ".logins[{"+LOGIN_DURATIONS_COL.APPID+"}]"
            + ".withinTimeframe["+df_timeframe+"]",
        LOGIN_DURATIONS_COL.DURATION,
        TotalAttributeContent
    )


def derive_dimensional_attributes_for_daily_login_counts(sessions_df: pd.DataFrame, df_timeframe: str = "eternally") -> List[ObservedProfileAttribute]:
    daily_login_counts_df = implicit_attribute_builder_utils.derive_daily_login_counts(sessions_df)
    return attribute_builder_utils.derive_dimensional_observed_attributes_from_df(
        daily_login_counts_df,
        [
            DAILY_LOGIN_COUNTS_COL.PROFILEID,
            DAILY_LOGIN_COUNTS_COL.APPID
        ],
        "countOf"
            + ".dailyLogins[{"+DAILY_LOGIN_COUNTS_COL.APPID+"}]"
            + ".withinTimeframe["+df_timeframe+"]",
        DAILY_LOGIN_COUNTS_COL.DAY,
        DAILY_LOGIN_COUNTS_COL.TOTAL,
        CONTEXTS.DAY,
        CounterAttributeContent,
        False
    )


def derive_dimensional_attributes_for_daily_login_durations(sessions_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:
    login_counts_df = implicit_attribute_builder_utils.derive_daily_login_duration(sessions_df)
    return attribute_builder_utils.derive_dimensional_observed_attributes_from_df(
        login_counts_df,
        [
            DAILY_LOGIN_DURATIONS_COL.PROFILEID,
            DAILY_LOGIN_DURATIONS_COL.APPID
        ],
        "durationOf"
            + ".dailyLogins[{"+DAILY_LOGIN_DURATIONS_COL.APPID+"}]"
            + ".withinTimeframe["+df_timeframe+"]",
        DAILY_LOGIN_DURATIONS_COL.DAY,
        DAILY_LOGIN_DURATIONS_COL.DURATION,
        CONTEXTS.DAY,
        TotalAttributeContent,
        False
    )


# TODO ... averages arent really counters ... make this more numerical or something ...
def derive_average_attributes_for_daily_login_counts(sessions_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:
    average_of_login_counts_df = implicit_attribute_builder_utils.derive_average_of_daily_login_counts(sessions_df)
    return attribute_builder_utils.derive_simple_observed_attributes_from_df(
        average_of_login_counts_df,
        [
            DAILY_LOGIN_COUNTS_COL.PROFILEID,
            DAILY_LOGIN_COUNTS_COL.APPID
        ],
        "averageCountOf"
            + ".dailyLogins[{"+DAILY_LOGIN_COUNTS_COL.APPID+"}]"
            + ".withinTimeframe["+df_timeframe+"]",
        DAILY_LOGIN_COUNTS_COL.TOTAL,
        AverageAttributeValue
    )


# TODO ... averages arent really counters ... make this more numerical or something ...
def derive_average_attributes_for_daily_login_duration(sessions_df:pd.DataFrame, df_timeframe:str="eternally") -> List[ObservedProfileAttribute]:
    average_of_login_duration_df = implicit_attribute_builder_utils.derive_average_of_daily_login_durations(sessions_df)
    return attribute_builder_utils.derive_simple_observed_attributes_from_df(
        average_of_login_duration_df,
        [
            DAILY_LOGIN_DURATIONS_COL.PROFILEID,
            DAILY_LOGIN_DURATIONS_COL.APPID
        ],
        "averageDurationOf"
            + ".dailyLogins[{"+DAILY_LOGIN_DURATIONS_COL.APPID+"}]"
            + ".withinTimeframe["+df_timeframe+"]",
        DAILY_LOGIN_DURATIONS_COL.DURATION,
        AverageAttributeValue
    )
