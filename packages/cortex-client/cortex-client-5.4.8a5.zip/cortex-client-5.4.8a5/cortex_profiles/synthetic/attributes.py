from typing import List, Tuple

from cortex_profiles.synthetic.insights import InsightsProvider
from cortex_profiles.synthetic.interactions import InteractionsProvider
from cortex_profiles.synthetic.profiles import ProfileProvider
from cortex_profiles.synthetic.sessions import SessionsProvider
from cortex_profiles.types.insights import Insight
from cortex_profiles.types.interactions import Session, InsightInteractionEvent
from faker import Factory
from faker.providers import BaseProvider

import pandas as pd
from cortex_profiles.utils_for_dfs import list_of_attrs_to_df

from cortex_profiles import implicit_attribute_builders
from cortex_profiles.types.attributes import ProfileAttribute

fake = Factory.create()
fake.add_provider(ProfileProvider)
fake.add_provider(InsightsProvider)
fake.add_provider(InteractionsProvider)
fake.add_provider(SessionsProvider)



class AttributeProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(AttributeProvider, self).__init__(*args, **kwargs)

    def data_to_build_single_profile(self, profileId:str=None) -> Tuple[str, List[Session], List[Insight], List[InsightInteractionEvent]]:
        profileId = profileId if profileId else fake.profileId()
        sessions = fake.sessions(profileId=profileId)
        insights = fake.insights(profileId=profileId)
        interactions = fake.interactions(profileId, sessions, insights)
        return (profileId, sessions, insights, interactions)

    def dfs_to_build_single_profile(self, profileId:str=None) -> Tuple[str, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        profileId, sessions, insights, interactions = self.data_to_build_single_profile(profileId=profileId)
        return (
            profileId, list_of_attrs_to_df(sessions), list_of_attrs_to_df(insights), list_of_attrs_to_df(interactions)
        )

    def attributes_for_single_profile(self, profileId:str=None) -> List[ProfileAttribute]:
        (profileId, sessions_df, insights_df, interactions_df) = self.dfs_to_build_single_profile(profileId=profileId)
        return implicit_attribute_builders.derive_implicit_attributes(insights_df, interactions_df, sessions_df)


if __name__ == "__main__":
    from faker import Factory
    f = Factory.create()
    f.add_provider(AttributeProvider)
    print(f.attributes_for_single_profile())

