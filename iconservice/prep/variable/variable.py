# Copyright 2019 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import TYPE_CHECKING, Optional, List

from .variable_storage import GovernanceVariable, VariableStorage
from ...icon_constant import ConfigKey

if TYPE_CHECKING:
    from ...iconscore.icon_score_context import IconScoreContext
    from ...database.db import ContextDatabase
    from .variable_storage import PReps, PRep
    from iconcommons import IconConfig


class Variable(object):

    def __init__(self, db: 'ContextDatabase'):
        self._storage: 'VariableStorage' = VariableStorage(db)

    def init_config(self, context: 'IconScoreContext', conf: 'IconConfig'):
        if self._storage.get_gv(context) is None:
            gv: 'GovernanceVariable' = GovernanceVariable.from_config_data(conf[ConfigKey.GOVERNANCE_VARIABLE])
            if gv.incentive_rep <= 0:
                raise Exception
            self._storage.put_gv(context, gv)

        if self._storage.get_prep_period(context) is None:
            prep_period: int = conf[ConfigKey.IISS_PREP_PERIOD]
            self._storage.put_prep_period(context, prep_period)

    def put_gv(self, context: 'IconScoreContext', gv: 'GovernanceVariable'):
        self._storage.put_gv(context, gv)

    def get_gv(self, context: 'IconScoreContext') -> 'GovernanceVariable':
        value: Optional['GovernanceVariable'] = self._storage.get_gv(context)
        if value is None:
            return GovernanceVariable()
        return value

    def put_preps(self, context: 'IconScoreContext', preps: 'PReps'):
        self._storage.put_preps(context, preps)

    def get_preps(self, context: 'IconScoreContext') -> List['PRep']:
        value: Optional['PReps'] = self._storage.get_preps(context)
        if value is None:
            return []
        return value.preps

    def put_prep_period(self, context: 'IconScoreContext', pre_period: int):
        self._storage.put_prep_period(context, pre_period)

    def get_prep_period(self, context: 'IconScoreContext') -> int:
        return self._storage.get_prep_period(context)
