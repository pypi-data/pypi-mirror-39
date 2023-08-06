from collections import defaultdict
from typing import List, Mapping

import arrow
from cortex_profiles.schemas.dataframes import INTERACTION_DURATIONS_COLS
from cortex_profiles.synthetic.apps import AppProvider
from cortex_profiles.types.insights import Insight
from cortex_profiles.types.interactions import Session, InsightInteractionEvent
from cortex_profiles.utils import get_until, flatten_list_recursively, reverse_index_dictionary, partition_list, \
    pick_random_time_between, group_by_key, unique_id
from faker import Factory, Generator
from faker.providers import BaseProvider

fake = Factory.create()
fake.add_provider(AppProvider)

# Todo - do all presented insights have to be either viewed or ignored?

interactions = [
    {
        "interaction": "presented",
        "subsetOf": [],
        "mutuallyExlusiveOf": []
    },
    {
        "interaction": "viewed",
        "subsetOf": [("presented", 10, 25)],
        "mutuallyExlusiveOf": ["ignored"]
    },
    {
        "interaction": "ignored",
        "subsetOf": [("presented", 10, 25)],
        "mutuallyExlusiveOf": ["viewed"]
    },
    {
        "interaction": "liked",
        "subsetOf": [("viewed", 10, 50)],
        "mutuallyExlusiveOf": ["disliked"]
    },
    {
        "interaction": "disliked",
        "subsetOf": [("viewed", 10, 35)],
        "mutuallyExlusiveOf": ["liked"]
    }
]


def randomly_choose_subset_of_list(fake:Generator, list_to_pick_from:List, list_to_ignore: List, min_num_of_elements:int, max_num_of_elements:int):
    num_of_elements = fake.random.randint(min_num_of_elements, max_num_of_elements)
    return  list(get_until(
        lambda: fake.random.choice(list_to_pick_from),
        appender=lambda obj, id_list: id_list + [obj],
        ignore_condition=lambda obj, id_list: obj in id_list or obj in list_to_ignore,
        stop_condition=lambda id_list: len(id_list) >= num_of_elements,
        to_yield=[]
    ))


class InteractionsProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(InteractionsProvider, self).__init__(*args, **kwargs)
        # self.companies = get_companies()

    # Build Interactions for Single Profile ...
    #     Get insights for profile
        # Choose which of the insights that get presetned ...
        # of the presented insights, choose which ones get viewed ...
        # of the viewed, get which ones get liked,
    #     Get sessions for profile
    #     Distribute different interactions on different insgihts ...
    #           Make sure there is atleast one presented insight per interaction?

    # Make sure view interactions happen after presented interactions ...
    # def interaction(self, interactionType, session, ):

    def raw_insight_distributions(self, insights:List[Insight]) -> Mapping[str,List]:
        distribution = defaultdict(list)
        insight_ids = map(lambda x: x.id, insights)
        for interaction in interactions:
            if not(interaction["subsetOf"]):
                ids_to_ignore = flatten_list_recursively([distribution[to_ignore] for to_ignore in interaction["mutuallyExlusiveOf"]])
                distribution[interaction["interaction"]].extend([id for id in insight_ids if id not in ids_to_ignore])
            else:
                ids_to_ignore = flatten_list_recursively([distribution[to_ignore] for to_ignore in interaction["mutuallyExlusiveOf"]])
                for subsetInteraction, minPercent, maxPercent in interaction["subsetOf"]:
                    min_elements_to_pick = int(len(distribution[subsetInteraction]) * minPercent / 100.0)
                    max_elements_to_pick = int(len(distribution[subsetInteraction]) * maxPercent / 100.0)
                    distribution[interaction["interaction"]].extend(randomly_choose_subset_of_list(
                        fake,
                        distribution[subsetInteraction],
                        ids_to_ignore,
                        min_elements_to_pick,
                        max_elements_to_pick
                    ))
        return distribution

    def insight_distributions(self, insights: List[Insight]) -> Mapping[str, List]:
        return reverse_index_dictionary(self.raw_insight_distributions(insights))

    def interaction_properties(self, interactionType:str, interactionStartTime:arrow.Arrow, maxInteractionEndTime:arrow.Arrow) -> dict:
        if interactionType != "viewed":
            return {}
        else:
            return {
                INTERACTION_DURATIONS_COLS.STARTED_INTERACTION: str(interactionStartTime),
                INTERACTION_DURATIONS_COLS.STOPPED_INTERACTION: str(pick_random_time_between(fake, interactionStartTime, maxInteractionEndTime))
            }

    def interaction(self, profileId:str, insightId:str, interactions_on_insight:List[str], sessions:List[Session]):
        """
        Assumption:
            - Sessions are from the same app ...
                Rational ... we might assign viewed insights event, and a presented in different sessions ... and they need to be from same app ..

        :param sessions:
        :param insightId:
        :param interactions_on_insight:
        :return:
        """
        partitioned_sessions = partition_list(sessions, len(interactions_on_insight))
        sessions_for_interaction_events = [
            fake.random.choice(partitioned_sessions[index])
            for index, interaction in enumerate(interactions_on_insight)
        ]
        interaction_times = [
            pick_random_time_between(fake, session.isoUTCStartTime, session.isoUTCEndTime)
            for session in sessions_for_interaction_events
        ]
        return [
            InsightInteractionEvent(
                id=unique_id(),
                sessionId=session.id,
                profileId=profileId,
                insightId=insightId,
                interactionType=interaction,
                interactionDateISOUTC=str(interactionTime),
                properties=self.interaction_properties(interaction, interactionTime, session.isoUTCEndTime),
                custom={},
            )
            for interaction, session, interactionTime in zip(interactions_on_insight, sessions_for_interaction_events, interaction_times)
        ]

    def interactions(self, profileId:str, profileSpecificSessions:List[Session], profileSpecificInsights:List[Insight]):
        """
        Assumption:
            - The sessions are for a specific profile.
            - The insights are for a specific profile.
        :param sessions:
        :param insights:
        :return:
        """
        insight_distributions = self.insight_distributions(profileSpecificInsights)
        app_distributed_sessions = group_by_key(profileSpecificSessions, lambda s: s.appId)
        return flatten_list_recursively([
            self.interaction(profileId, insightId, interactions_on_insight, profileAndAppSpecificSessions)
            for insightId, interactions_on_insight in insight_distributions.items()
            for appId, profileAndAppSpecificSessions in app_distributed_sessions.items()
        ])



if __name__ == "__main__":
    from cortex_profiles.synthetic.tests import test_insight_distribution, test_insight_interaction_events
    test_insight_distribution()
    test_insight_interaction_events()