from faker.providers import BaseProvider
from faker import Factory
from cortex_profiles.utils import MappableList

fake = Factory.create()

apps = [ "FNI", "CTI" ]
# apps = [ "FNI", "CTI", "Jarvis", "Oragami", "Macys", "GolfNow" ]


class AppProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(AppProvider, self).__init__(*args, **kwargs)


    def appId(self):
        return "{}:{}".format(fake.random.choice(apps), "1.0.0")

    def detailedAppId(self):
        return "{}:{}".format(fake.random.choice(apps), self.symanticVersion())

    def symanticVersion(self):
        return fake.random.choice([
            "{}.{}.{}-alpha".format(fake.random.randint(0, 5), fake.random.randint(0, 10), fake.random.randint(0, 10)),
            "{}.{}.{}-alpha.{}".format(fake.random.randint(0, 5), fake.random.randint(0, 10), fake.random.randint(0, 100), fake.random.randint(0, 10)),
            "{}.{}.{}-alpha.beta".format(fake.random.randint(0, 5), fake.random.randint(0, 10), fake.random.randint(0, 10)),
            "{}.{}.{}-beta".format(fake.random.randint(0, 5), fake.random.randint(0, 10), fake.random.randint(0, 10)),
            "{}.{}.{}-beta.{}".format(fake.random.randint(0, 5), fake.random.randint(0, 10), fake.random.randint(0, 100), fake.random.randint(0, 10)),
            "{}.{}.{}-rc.{}".format(fake.random.randint(0, 5), fake.random.randint(0, 10), fake.random.randint(0, 100), fake.random.randint(0, 10)),
            "{}.{}.{}".format(fake.random.randint(0, 5), fake.random.randint(0, 10), fake.random.randint(0, 10)),
        ])


if __name__ == "__main__":
    # from cortex_profiles.synthetic.concepts import CortexConceptsProvider
    from faker import Factory
    f = Factory.create()
    f.add_provider(AppProvider)
    for x in range(0, 100):
        print(f.appId())
