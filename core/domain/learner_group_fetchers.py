# coding: utf-8
#
# Copyright 2022 The Oppia Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Getter commands for learner group models."""

from __future__ import annotations

from core.domain import learner_group_domain
from core.domain import learner_group_services
from core.platform import models

from typing import List, Optional

MYPY = False
if MYPY: # pragma: no cover
    from mypy_imports import learner_group_models
    from mypy_imports import user_models

(learner_group_models, user_models) = models.Registry.import_models(
    [models.NAMES.learner_group, models.NAMES.user])


def get_new_learner_group_id() -> str:
    """Returns a new learner group id.

    Returns:
        str. A new learner group id.
    """
    return learner_group_models.LearnerGroupModel.get_new_id()


def get_learner_group_by_id(
    group_id: str
) -> Optional[learner_group_domain.LearnerGroup]:
    """Returns the learner group domain object given the learner group id.

    Args:
        group_id: str. The id of the learner group.

    Returns:
        LearnerGroup or None. The learner group domain object corresponding to
        the given id or None if no learner group exists for the given group id.
    """
    learner_group_model = learner_group_models.LearnerGroupModel.get(
        group_id, strict=False)

    if not learner_group_model:
        return None

    return learner_group_services.get_learner_group_from_model(
        learner_group_model)


def get_learner_groups_of_facilitator(
    user_id: str
) -> List[learner_group_domain.LearnerGroup]:
    """Returns a list of learner groups of the given facilitator.

    Args:
        user_id: str. The id of the facilitator.

    Returns:
        list(LearnerGroup). A list of learner groups of the given facilitator.
    """
    learner_grp_models = (
        learner_group_models.LearnerGroupModel.get_by_facilitator_id(user_id))

    if not learner_grp_models:
        return []

    return [
        learner_group_services.get_learner_group_from_model(model)
        for model in learner_grp_models
    ]


def can_multi_learners_share_progress(
    user_ids: List[str], group_id: str
) -> List[bool]:
    """Returns the progress sharing permissions of the given users in the given
    group.

    Args:
        user_ids: list(str). The user ids of the learners of the group.
        group_id: str. The id of the learner group.

    Returns:
        list(bool). True if a user has progress sharing permission of the
        given group as True, False otherwise.
    """
    learner_group_user_models = user_models.LearnerGroupsUserModel.get_multi(
        user_ids
    )

    progress_sharing_permissions: List[bool] = []
    for model in learner_group_user_models:
        # Ruling out the possibility of None for mypy type checking.
        assert model is not None
        for group_details in model.learner_groups_user_details:
            if group_details['group_id'] == group_id:
                progress_sharing_permissions.append(
                    bool(group_details['progress_sharing_is_turned_on'])
                )
                break

    return progress_sharing_permissions
