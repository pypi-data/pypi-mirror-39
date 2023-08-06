import arrow
from typing import List, Tuple
from cortex_profiles.synthetic.apps import AppProvider
from cortex_profiles.synthetic.concepts import CortexConceptsProvider
from cortex_profiles.synthetic.profiles import ProfileProvider
from cortex_profiles.utils import get_until, unique_id, seconds_between_times
from cortex_profiles.types.interactions import Session
from faker import Factory
from faker.providers import BaseProvider

fake = Factory.create()
fake.add_provider(CortexConceptsProvider)
fake.add_provider(ProfileProvider)
fake.add_provider(AppProvider)


def x_inbetween_range(x, rng):
    start_rng = min(list(rng))
    stop_rng = max(list(rng))
    return (x >= start_rng and x <= stop_rng)


def time_tuples_intersect(tupleA, tupleB) -> bool:
    start_a = min(list(tupleA))
    stop_a = max(list(tupleA))
    start_b = min(list(tupleB))
    stop_b = max(list(tupleB))
    return (
        x_inbetween_range(start_a, tupleB) or
        x_inbetween_range(stop_a, tupleB) or
        x_inbetween_range(start_b, tupleA) or
        x_inbetween_range(stop_b, tupleA)
    )


def session_overlaps_with_other_sessions(session, session_list) -> bool:
    if not session_list:
        return False
    return any(time_tuples_intersect(session, s) for s in session_list)


def random_date_within_past_x_days(days:int) -> arrow.Arrow:
    return arrow.utcnow().shift(days=(-1*fake.random.randint(1, days+1)), seconds=fake.random.randint(1, 86400))


class SessionsProvider(BaseProvider):

    def __init__(self, *args, **kwargs):
        super(SessionsProvider, self).__init__(*args, **kwargs)

    def session_time(self, min_length_in_seconds=180, max_length_in_seconds=7200):
        session_start=random_date_within_past_x_days(days=30)
        session_length=fake.random.randint(min_length_in_seconds, max_length_in_seconds)
        return (session_start, session_start.shift(seconds=session_length))

    # TODO ... optimize this ... it takes too long for a session ...
    def session_times(self) -> List[Tuple[arrow.Arrow, arrow.Arrow]]:
        total_sessions_for_user = fake.random.randint(1, 100)
        return list(sorted(
            get_until(
                self.session_time,
                appender=lambda obj, session_list: session_list + [obj],
                ignore_condition=session_overlaps_with_other_sessions,
                stop_condition=lambda session_list: len(session_list) >= total_sessions_for_user,
                to_yield=[]
            ),
            key=lambda x: x[0]
        ))

    def session(self, start_time:arrow.Arrow, stop_time:arrow.Arrow, profileId:str=None) -> Session:
        return Session(
            id=unique_id(),
            profileId=profileId if profileId else fake.profileId(),
            appId=fake.appId(),
            isoUTCStartTime=start_time,
            isoUTCEndTime=stop_time,
            durationInSeconds=seconds_between_times(start_time, stop_time)
        )

    def sessions(self, profileId:str=None) -> List[Session]:
        return [
            self.session(start_time, stop_time, profileId=profileId) for start_time, stop_time in self.session_times()
        ]


if __name__ == "__main__":
    from faker import Factory
    f = Factory.create()
    f.add_provider(SessionsProvider)
    for x in range(0, 5):
        print(f.sessions())
