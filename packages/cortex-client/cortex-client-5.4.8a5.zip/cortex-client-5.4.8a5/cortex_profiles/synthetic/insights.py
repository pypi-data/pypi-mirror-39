from faker.providers import BaseProvider
from faker import Factory
from cortex_profiles.utils import MappableList, List, pick_random_time_between
from cortex_profiles.types.insights import InsightTag, Link, Insight
from cortex_profiles.synthetic.concepts import CortexConceptsProvider
from cortex_profiles.synthetic.profiles import ProfileProvider
from cortex_profiles.synthetic.apps import AppProvider

from cortex_profiles.schemas.schemas import CONTEXTS
from uuid import uuid4


import arrow


fake = Factory.create()
fake.add_provider(CortexConceptsProvider)
fake.add_provider(ProfileProvider)
fake.add_provider(AppProvider)

insight_types = {
    "CTI": [
        "RetirementInsights",
        "FundOptimizationInsights"
        "InvestmentInsights",
    ],
    "FNI": [
        "FinancialNewsInsights",
        "CompanyMergerInsights",
        "CLevelChangeInsights",
    ]
}

class InsightsProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(InsightsProvider, self).__init__(*args, **kwargs)

    def insightId(self):
        return str(uuid4())

    def insightType(self, appId:str):
        app_specific_insight_type = insight_types[appId.split(":")[0]]
        return fake.random.choice(app_specific_insight_type)

    def tag(self, insightId:str, taggedOn:str) -> InsightTag:
        return InsightTag(
            id=str(uuid4()),
            insight=Link(
                id=insightId,
                context=CONTEXTS.INSIGHT
            ),
            tagged=taggedOn,
            concept=fake.concept(),
            relationship=Link(
                id=CONTEXTS.INSIGHT_TAG_RELATED_TO_RELATIONSHIP,
                context=CONTEXTS.INSIGHT_TAG_RELATIONSHIP,
            )
        )

    def tags(self, insightId:str, taggedOn:str) -> List[InsightTag]:
        return [self.tag(insightId, taggedOn) for x in range(0, fake.random.randint(0,10))]

    def insight(self, profileId) -> Insight:
        insightId = self.insightId()
        appId = fake.appId()
        dateGenerated = str(pick_random_time_between(fake, arrow.utcnow().shift(days=-30), arrow.utcnow()))
        return Insight(
            id=insightId,
            tags=self.tags(insightId, dateGenerated),
            insightType=self.insightType(appId=appId),
            profileId=profileId,
            dateGeneratedUTCISO=dateGenerated,
            appId=appId
        )

    def insights(self, profileId:str=None, floor:int=100, ceiling:int=10000) -> List[Insight]:
        profileId = profileId if profileId else fake.profileId()
        return [
            self.insight(profileId=profileId)
            for x in range(0, fake.random.randint(floor, ceiling))
        ]


if __name__ == "__main__":
    from faker import Factory
    f = Factory.create()
    f.add_provider(InsightsProvider)
    for x in range(0, 100):
        print(f.insight())

