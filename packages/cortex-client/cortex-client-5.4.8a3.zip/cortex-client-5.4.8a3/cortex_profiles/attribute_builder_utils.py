import uuid
from typing import List

import attr
import pandas as pd
from cortex_profiles import utils, utils_for_dfs
from cortex_profiles.schemas.schemas import CONTEXTS
from cortex_profiles.types.attribute_values import ObjectValue, DimensionalAttributeContent, Dimension
from cortex_profiles.types.attributes import ObservedProfileAttribute, DeclaredProfileAttribute


def derive_dimensional_observed_attributes_from_df(
        df:pd.DataFrame, attribute_identifiers:List[str], attributeKeyPattern:str,
        dimensionIDColumn:str, dimensionValueColumn:str,
        contextOfDimension:str, classOfDimensionValue:str,
        isColumnForDimensionContext:bool=True,
        profileType:str= CONTEXTS.END_USER_PROFILE
    ) -> List[ObservedProfileAttribute]:
    return [
        derive_observed_dimensional_attributes_from_grouped_df(
            gdf, attribute_identifiers, list(gid), attributeKeyPattern,
            dimensionIDColumn, dimensionValueColumn,
            contextOfDimension, classOfDimensionValue, isColumnForDimensionContext, profileType)
        for gid, gdf in df.groupby(attribute_identifiers, as_index=False)
    ]


def derive_observed_dimensional_attributes_from_grouped_df(
        grouped_df:pd.DataFrame, group_id_keys:List, group_id_values:List, attributeKeyPattern:str,
        dimensionIDColumn:str, dimensionValueColumn:str, contextOfDimension:str, classOfDimensionValue:str,
        isColumnForDimensionContext:bool=False, profileType:str= CONTEXTS.END_USER_PROFILE) -> ObservedProfileAttribute:
    if grouped_df.empty:
        return None
    assert "profileId" in grouped_df.columns, "ProfileId must be in dataframe ..."
    identifier = dict(zip(group_id_keys, group_id_values))
    attributeValue = DimensionalAttributeContent(
        contextOfDimension=identifier[contextOfDimension] if isColumnForDimensionContext else contextOfDimension,
        contextOfDimensionValue=attr.fields(classOfDimensionValue).context.default,
        value=list(sorted(
            [
                Dimension(dimensionId=x, dimensionValue=y)
                for x, y in utils_for_dfs.df_to_tuples(grouped_df, [dimensionIDColumn, dimensionValueColumn])
            ],
            key=lambda d: -1 * d.dimensionValue
        ))
    )
    return ObservedProfileAttribute(
        id=str(uuid.uuid4()),
        attributeKey=attributeKeyPattern.format(**identifier),
        profileId=str(identifier["profileId"]),
        profileType=profileType,
        createdAt=utils.utc_timestamp(),
        observedAt=utils.utc_timestamp(),
        attributeValue=attributeValue,
        # valueSummary=attributeValue.summarize()
    )


def derive_simple_observed_attributes_from_df(
        df:pd.DataFrame,
        attribute_identifiers:List[str],
        attributeKeyPattern:str,
        valueColumn:str,
        classOfValue:type,
        profileType:str= CONTEXTS.END_USER_PROFILE
    ) -> List[ObservedProfileAttribute]:
    return [
        derive_simple_observed_attributes_from_grouped_df(
            gdf, attribute_identifiers, list(gid), attributeKeyPattern,
            valueColumn, classOfValue, profileType)
        for gid, gdf in df.groupby(attribute_identifiers, as_index=False)
    ]


def derive_simple_observed_attributes_from_grouped_df(
        grouped_df:pd.DataFrame, group_id_keys:List, group_id_values:List,
        attributeKeyPattern:str, counterColumn:str, classOfValue:type,
        profileType:str= CONTEXTS.END_USER_PROFILE) -> ObservedProfileAttribute:
    if grouped_df.empty:
        return []
    assert "profileId" in grouped_df.columns, "profileId must be a column in the dataframe ..."
    identifier = dict(zip(group_id_keys, group_id_values))
    attributeValue = classOfValue(
        value=sum(grouped_df[counterColumn])
    )
    return ObservedProfileAttribute(
        id=utils.unique_id(),
        attributeKey=attributeKeyPattern.format(**identifier),
        profileId=str(identifier["profileId"]),
        profileType=profileType,
        createdAt=utils.utc_timestamp(),
        observedAt=utils.utc_timestamp(),
        attributeValue=attributeValue,
        # valueSummary=attributeValue.summarize()
    )


def derive_declared_attributes_from_key_value_df(
        declarations:pd.DataFrame, profileIdColumn:str="profileId",
        keyColumn:str="key", valueColumn:str="value", attributeValueClass:type=ObjectValue,
        profileType:str= CONTEXTS.END_USER_PROFILE
    ) -> List[DeclaredProfileAttribute]:
    return [
        DeclaredProfileAttribute(
            id=utils.unique_id(),
            attributeKey=rec[keyColumn],
            profileId=str(rec[profileIdColumn]),
            profileType=profileType,
            createdAt=utils.utc_timestamp(),
            declaredAt=utils.utc_timestamp(),
            attributeValue=attributeValueClass(rec[valueColumn]),
            # valueSummary=attributeValueClass(rec[valueColumn]).summarize()
        )
        for rec in utils_for_dfs.df_to_records(declarations)
    ]

def derive_declared_attributes_from_value_only_df(
        declarations:pd.DataFrame,
        profileIdColumn:str="profileId",
        key:str="key",
        valueColumn:str="value",
        attributeValueClass:type=ObjectValue,
        profileType:str= CONTEXTS.END_USER_PROFILE
    ) -> List[DeclaredProfileAttribute]:
    return [
        DeclaredProfileAttribute(
            id=utils.unique_id(),
            attributeKey=key,
            profileId=str(rec[profileIdColumn]),
            profileType=profileType,
            createdAt=utils.utc_timestamp(),
            declaredAt=utils.utc_timestamp(),
            attributeValue=attributeValueClass(rec[valueColumn]),
            # valueSummary=attributeValueClass(rec[valueColumn]).summarize()
        )
        for rec in utils_for_dfs.df_to_records(declarations)
    ]



def derive_quantile_config_for_column(df:pd.DataFrame, column_name:str, quantile_config:dict) -> pd.Series:
    return {
        key: list(map(lambda x: df[column_name].quantile(x), values)) for key, values in quantile_config.items()
    }


def determine_bucket_from_quartile_config(value:object, config:dict) -> str:
    # Taking tail for values on the edge to be more generous
    return [key for key, values in config.items() if (value >= values[0] and value <= values[1])][-1]


def high_med_low_bucket(df:pd.DataFrame, column_name:str, quantile_config:dict) -> pd.Series:
    return df[column_name].map(lambda x: determine_bucket_from_quartile_config(x, quantile_config))