from cortex_profiles.synthetic.attributes import AttributeProvider
from cortex_profiles.synthetic.profiles import ProfileProvider
from cortex_profiles.synthetic.insights import InsightsProvider
from cortex_profiles.synthetic.sessions import SessionsProvider
from cortex_profiles.synthetic.apps import AppProvider
from cortex_profiles.synthetic.interactions import InteractionsProvider
from cortex_profiles.synthetic.concepts import CortexConceptsProvider

from faker import Factory, Generator


def add_profile_providers(fake:Generator) -> None:
    fake.add_provider(AttributeProvider)
    fake.add_provider(ProfileProvider)
    fake.add_provider(InsightsProvider)
    fake.add_provider(SessionsProvider)
    fake.add_provider(AppProvider)
    fake.add_provider(InteractionsProvider)
    fake.add_provider(CortexConceptsProvider)

profile_synthesizer = Factory.create()
add_profile_providers(profile_synthesizer)

