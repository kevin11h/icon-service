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


from typing import Any, Optional, TYPE_CHECKING

from .value import SystemValue
from ..base.ComponentBase import StorageBase
from ..database.db import ContextDatabase
from ..icon_constant import SystemValueType
from ..utils.msgpack_for_db import MsgPackForDB


if TYPE_CHECKING:
    from ..iconscore.icon_score_context import IconScoreContext


class Storage(StorageBase):
    PREFIX: bytes = b'gv'
    MIGRATION_FLAG: bytes = b'mf'

    def __init__(self, db: 'ContextDatabase'):
        super().__init__(db)

    # Todo: move to the system engine
    def load_system_value(self, context: 'IconScoreContext') -> 'SystemValue':
        is_migrated: bool = self.get_migration_flag(context)
        system_value: Optional['SystemValue'] = None
        if not is_migrated:
            return system_value

        # load from the db
        return system_value

    def get_migration_flag(self, context: 'IconScoreContext') -> bool:
        return bool(self._db.get(context, self.PREFIX + self.MIGRATION_FLAG))

    def put_migration_flag(self, context: 'IconScoreContext') -> bool:
        return bool(self._db.put(context, self.PREFIX + self.MIGRATION_FLAG, MsgPackForDB.dumps(True)))

    def put_value(self, context: 'IconScoreContext', type: 'SystemValueType', value: Any):
        assert isinstance(type, SystemValueType)
        self._db.put(context, self.PREFIX + type.value, MsgPackForDB.dumps(value))

    def get_value(self, context: 'IconScoreContext', type: 'SystemValueType'):
        assert isinstance(type, SystemValueType)
        value: Any = self._db.get(context, self.PREFIX + type.value)
        # Todo: check this point
        return MsgPackForDB.loads(value)