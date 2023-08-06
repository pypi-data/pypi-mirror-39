
def test_insight_distribution():
    from faker import Factory
    from cortex_profiles.synthetic.insights import InsightsProvider
    from cortex_profiles.synthetic.interactions import InteractionsProvider, interactions
    f = Factory.create()
    f.add_provider(InsightsProvider)
    f.add_provider(InteractionsProvider)

    derived_interactions = f.raw_insight_distributions(f.insights("abc"))
    for i in interactions:
        assert len(derived_interactions[i["interaction"]]) == len(set(derived_interactions[i["interaction"]]))

    mutually_exclusive_pairs = [
        (i["interaction"], me)
        for i in interactions
        for me in i["mutuallyExlusiveOf"]
        if i["mutuallyExlusiveOf"]
    ]
    print(mutually_exclusive_pairs)
    for me_a, me_b in mutually_exclusive_pairs:
        assert len(set(derived_interactions[me_a]).intersection(
            set(derived_interactions[me_b]))) == 0, "{} and {} are not mutually exclusive".format(me_a, me_b)

    print(f.insight_distributions(f.insights("abc")))


def test_insight_interaction_events():
    from faker import Factory
    from cortex_profiles.synthetic.sessions import SessionsProvider
    from cortex_profiles.synthetic.insights import InsightsProvider
    from cortex_profiles.synthetic.interactions import InteractionsProvider

    f = Factory.create()
    f.add_provider(InsightsProvider)
    f.add_provider(InteractionsProvider)
    f.add_provider(SessionsProvider)

    print(f.interactions("test-user-1", f.sessions("test-user-1"), f.insights(profileId="test-user-1")))



