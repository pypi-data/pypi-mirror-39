from faker.providers import BaseProvider
from faker import Factory

from cortex_profiles.utils import get_unique_cortex_objects
from cortex_profiles.types.insights import Link
from cortex_profiles.schemas.schemas import DOMAIN_CONCEPTS

from iso3166 import countries as countries

fake = Factory.create()


# TODO ... for the attribute building to work right ... the title needs to be the context of the tag ... not the name ...

def get_person() -> dict:
    return {
        "id": "{} {}".format(fake.first_name(), fake.last_name()),
        "context": DOMAIN_CONCEPTS.PERSON,
        "title": DOMAIN_CONCEPTS.PERSON,
    }


def get_company() -> dict:
    return {
        "id": fake.company(),
        "context": DOMAIN_CONCEPTS.COMPANY,
        "title": DOMAIN_CONCEPTS.COMPANY,
    }


def get_country() -> dict:
    country = countries.get(fake.country_code(representation='alpha-3'))
    return {
        "id": "{}({})".format(country.alpha3, country.name),
        "context": DOMAIN_CONCEPTS.COUNTRY,
        "title": DOMAIN_CONCEPTS.COUNTRY
    }


def get_currency() -> dict:
    currency = fake.currency()
    return {
        "id": "{}({})".format(currency[0], currency[1]),
        "context": DOMAIN_CONCEPTS.CURRENCY,
        "title": DOMAIN_CONCEPTS.CURRENCY,
    }


def get_website() -> dict:
    return {
        "id": "{0}".format(fake.url()),
        "context": DOMAIN_CONCEPTS.WEBSITE,
        "title": DOMAIN_CONCEPTS.WEBSITE
    }


class CortexConceptsProvider(BaseProvider):

    def __init__(self, *args,
                 people_limit=50, company_limit=50, country_limit=50, currency_limit=50, website_limit=50,
                 **kwargs):
        super(CortexConceptsProvider, self).__init__(*args, **kwargs)
        self.people = get_unique_cortex_objects(get_person, people_limit)
        self.companies = get_unique_cortex_objects(get_company, company_limit)
        self.countries = get_unique_cortex_objects(get_country, country_limit)
        self.currencies = get_unique_cortex_objects(get_currency, currency_limit)
        self.websites = get_unique_cortex_objects(get_website, website_limit)

    def person(self) -> Link:
        return Link(**fake.random.choice(self.people))

    def company(self) -> Link:
        return Link(**fake.random.choice(self.companies))

    def country(self) -> Link:
        return Link(**fake.random.choice(self.countries))

    def currency(self) -> Link:
        return Link(**fake.random.choice(self.currencies))

    def website(self) -> Link:
        return Link(**fake.random.choice(self.websites))

    def concept(self) -> Link:
        return fake.random.choice([
            self.person,
            self.company,
            self.country,
            self.currency,
            self.website,
        ])()


if __name__ == "__main__":
    # from cortex_profiles.synthetic.concepts import CortexConceptsProvider
    from faker import Factory
    f = Factory.create()
    f.add_provider(CortexConceptsProvider)
    for x in range(0, 100):
        print(f.concept())
