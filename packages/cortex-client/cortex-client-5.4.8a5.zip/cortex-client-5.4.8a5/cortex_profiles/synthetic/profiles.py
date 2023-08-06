from faker.providers import BaseProvider
from faker import Factory

from uuid import uuid4

fake = Factory.create()


class ProfileProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(ProfileProvider, self).__init__(*args, **kwargs)

    def profileId(self):
        return str(uuid4())


if __name__ == "__main__":
    # from cortex_profiles.synthetic.concepts import CortexConceptsProvider
    from faker import Factory
    f = Factory.create()
    f.add_provider(ProfileProvider)
    for x in range(0, 100):
        print(f.profileId())
