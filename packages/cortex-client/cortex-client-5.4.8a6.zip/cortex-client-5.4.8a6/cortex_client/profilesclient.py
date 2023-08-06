
"""
Copyright 2018 Cognitive Scale, Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""


import json
from typing import List, Optional, Tuple

import attr
import pandas as pd
from cortex_profiles.internalprofilesclient import InternalProfilesClient
from cortex_profiles.notebook.utils import InteractableJson
from cortex_profiles.notebook.utils import tab_with_content, to_output
from cortex_profiles.types.profiles import ProfileCommit, Profile, ProfileAttribute
from cortex_profiles.schemas.client_dataframes import COMMIT_COL, ATTRIBUTE_COL, PROFILE_COL
from .authenticationclient import AuthenticationClient
from .client import _Client

OrderedList = List


class ProfilesClient(_Client):
    """A client for the Cortex Profiles SDK Functionality."""

    def __init__(self, url:str, version:str, token:str, environmentId:str="cortex/default"):
        self.token = token
        self.authclient = AuthenticationClient(url, "2", token)
        self.tenantId = self.authclient.fetch_current_user_details()["tenant"]
        self._internal_profiles_client = InternalProfilesClient(url, version, token, environmentId)
        self.environmentId = environmentId

    def listCommits(self, profileId:str) -> Optional[Profile]:
        """
        Get Commit History ...
        :param profileId:
        :return:
        """
        return pd.DataFrame([
            {
                COMMIT_COL.COMMIT_ID: commit.id,
                COMMIT_COL.TIMESTAMP: commit.createdAt,
                COMMIT_COL.ATTRS_ADDED: len(commit.attributesAdded),
                COMMIT_COL.ATTRS_REMOVED: len(commit.attributesRemoved),
                COMMIT_COL.ATTRS_MODIFIED:len(commit.attributesModified)
            }
            for commit in self._internal_profiles_client.get_commit_history_for_profile(profileId)
        ], columns=list(COMMIT_COL.values())).sort_values(by=COMMIT_COL.TIMESTAMP, ascending=False)  # .set_index(["commitId"])

    def listAttributes(self, profileId:str, commitId:Optional[str]=None) -> Optional[Profile]:
        """
        Get the profile as of a certain commit
            ... defaults to latest commit if no commitId is specified ...
        :param profileId:
        :param commitId:
        :return:
        """
        profile = self.describeProfile(profileId, commitId)
        attributes = profile["attributes"] if profile else []
        return pd.DataFrame([
            {
                ATTRIBUTE_COL.ATTRIBUTE_KEY: attribute["attributeKey"],
                ATTRIBUTE_COL.ATTRIBUTE_ID: attribute["id"],
                ATTRIBUTE_COL.ATTRIBUTE_TYPE: attribute["context"],
                ATTRIBUTE_COL.ATTRIBUTE_VALUE_TYPE: attribute["attributeValue"]["context"]
            }
            for attribute in attributes
        ], columns=list(ATTRIBUTE_COL.values())).sort_values(by=[ATTRIBUTE_COL.ATTRIBUTE_KEY])

    def listProfiles(self, query:Optional[dict]=None):
        return pd.DataFrame(
            self._internal_profiles_client.list_profiles(query), columns=list(PROFILE_COL.values())
        ).sort_values(by=[PROFILE_COL.PROFILE_TYPE, PROFILE_COL.PROFILE_ID])


    def describeProfile(self, profileId:str, commitId:Optional[str]=None) -> Optional[Profile]:
        """
        Get the profile as of a certain commit
            ... defaults to latest commit if no commitId is specified ...
        :param profileId:
        :param commitId:
        :return:
        """
        profile = self._internal_profiles_client.get_profile(profileId, commitId)
        if profile:
            return attr.asdict(self._internal_profiles_client.expand_profile(profile))
        else:
            return None

    def describeCommit(self, commitId:str):
        """
        Describe a specific commit ...
        :param commitId:
        :return:
        """
        return self._internal_profiles_client.get_commit_by_id(commitId)

    def describeAttribute(self, profileId:str, attributekey:str, commitId:str=None):
        """
        Describe a specific commit ...
        :param attributekey:
        :return:
        """
        commit = (
            self._internal_profiles_client.get_latest_profile_commit(profileId)
            if not commitId else self._internal_profiles_client.get_commit_by_id(commitId)
        )
        if not commit:
            return None
        return self._internal_profiles_client.get_attribute_by_key(profileId, attributekey, commit.id)


    def visualizeHistoryOfAttribute(self, profileId:str, attributeKey:str):
        return tab_with_content({
            commitId: to_output(self._render_json(self.describeAttribute(profileId, attributeKey, commitId=commitId)))
            for commitId in reversed(self.listCommits(profileId)[COMMIT_COL.COMMIT_ID])
        })

    def visualizeHistoryOfAttributesInProfile(self, profileId:str):
        return tab_with_content({
            commitId: to_output(self.listAttributes(profileId, commitId=commitId))
            for commitId in reversed(self.listCommits(profileId)[COMMIT_COL.COMMIT_ID])
        })

    def visualizeHistoryOfCommitsOnProfile(self, profileId: str):
        return tab_with_content({
            commitId: to_output(self.listAttributes(profileId, commitId=commitId))
            for commitId in reversed(self.listCommits(profileId)[COMMIT_COL.COMMIT_ID])
        })

    def visualizeProfile(self, profileId:str, commitId:Optional[str]=None):
        return self._render_json(self.describeProfile(profileId, commitId))

    def pushAttributes(self, profileId:str, attributes:List[ProfileAttribute]) -> Tuple[str, Tuple[Profile, ProfileCommit]]:
        """
        Pushes attributes to the latest profile for the specified profileId
        :param profileId:
        :param attributes:
        :return:
        """
        return self._internal_profiles_client.append_attributes_to_profile(attributes, profileId)

    def findBottomProfilesForAttributeWithCounterValue(self, attributeKey: str, n=5):
        return pd.DataFrame([
            {
                "profileId": attribute["profileId"],
                "attributeKey": attribute["attributeKey"],
                "attributeValue": attribute["attributeValue"]["value"]
            }
            for attribute in self._internal_profiles_client.sort_counter_based_attributes(attributeKey, pick=n, ascending=True)
        ], columns=["profileId", "attributeKey", "attributeValue"])

    def findTopProfilesForAttributeWithCounterValue(self, attributeKey:str, n=5):
        return pd.DataFrame([
            {
                "profileId": attribute["profileId"],
                "attributeKey": attribute["attributeKey"],
                "attributeValue": attribute["attributeValue"]["value"]
            }
            for attribute in
            self._internal_profiles_client.sort_counter_based_attributes(attributeKey, pick=n, ascending=False)
        ], columns=["profileId", "attributeKey", "attributeValue"])

    def countsOfLatestAttributesPerProfile(self, query:Optional[dict]=None) -> pd.DataFrame:
        return pd.DataFrame(
            self._internal_profiles_client.counts_of_latest_attributes_per_profile(query),
            columns=["profileId", "profileType", "totalCountOfLatestAttributes"]
        )

    def _render_json(self, j:dict):

        return InteractableJson(json.loads(json.dumps(j)))
        # return pprint(utils.json_makeup(json.loads(json.dumps(j))))

    # TODO Link the commit history
    # Todo .. pull changes on profile as of latest commit ...
    #     Net attributes added ... download them and append them to the profile ..

    # def findProfilesWithAllAttributes(self, attributeKeys:List[str]):
    #     """
    #     Returns a list of profiles that have all of the attributes specified in their latest version.
    #     :param attributeKeys:
    #     :return:
    #     """
    #     pass
    #
    # def findProfilesWithSomeAttributes(self, attributeKeys:List[str]):
    #     """
    #     Returns a list of profiles that have all of the attributes specified in their latest version.
    #     :param attributeKeys:
    #     :return:
    #     """
    #     pass

    # def findProfilesWithAttributeQuery(self):


    # def findsCommitsBetweenDates

    # Todo link to find attributes ...
    # Todo ... link to ... find_latest_snapshot_for_profile
    # TODO - link to find query commits  in internal ......
    # TODO .. link to interla find profiles ...

    # def list_available_attributes_for_latest_profile(self, profileId: str) -> List[ProfileAttributeMapping]:
    #     # snapshot = find_latest_snapshot_for_profile(profileId, cortex)
    #     # if not snapshot:
    #     #     return []
    #     # return list(map(
    #     #     lambda attr: ProfileAttributeMapping(attributeKey=attr.attributeKey, attributeId=attr.id),
    #     #     snapshot.attributes
    #     # ))
    #     return [
    #         ProfileAttributeMapping(attributeKey=attribute.attributeKey, attributeId=attribute.id)
    #         for attribute in self._internal_profiles_client.find_latest_attributes_for_profile(profileId, [])
    #     ]

    # When we get history of a profile ...
    #   ... we get the latest commit for that profile and find all of the commits it was recursively involved in
    #   ... and get the commit id and time of each !
    # We can even turn this into a dataframe!


    # def merge_attributes_with_profile():
    #     """
    #     This attempts to merge two sets of profiles
    #     i.e ... two counters will get merged ...
    #     counters get merged ...
    #     latest is chosen for declared attributes ...
    #     :return:
    #     """
    #     pass


    # def net_attributes_from_commit_chain(commitChain: ProfileCommitChain) -> List[ProfileAttributeMapping]:
    #     """
    #     What are the net profile attributes after applying all of the changes
    #     in the commit chain?
    #     """
    #     snapshot = commitChain.snapshot
    #     # Start with attribute from profile snapshots ...
    #     attributes = snapshot.attributes
    #
    #     # Apply all of the additional commits on top of the snapshot ...
    #     attributes = flatmap(commitChain.additionalCommits, attributes, apply_commit_to_attributes)
    #     # Apply the latest commit
    #     attributes = apply_commit_to_attributes(attributes, )


    # def get_current_profile_attributes_for_user(profileId):
    #     pass
