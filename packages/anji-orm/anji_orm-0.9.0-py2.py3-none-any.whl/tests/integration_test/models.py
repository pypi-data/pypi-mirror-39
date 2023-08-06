from datetime import datetime
from enum import Enum
from typing import Dict, Optional

from aenum import Enum as AEnum
from anji_orm import Model, Field, IndexPolicy, IndexPolicySetting


class X1(Enum):

    t = 't'


class Y1(AEnum):

    t = 't'


class T1(Model):

    _table = 'test_table'

    _index_policy = IndexPolicy.singlemore
    _index_policy_settings = {
        IndexPolicySetting.additional_indexes: [
            ('c1:c2', ['c1', 'c2'])
        ]
    }

    c1: Optional[str] = Field(secondary_index=True)
    c2: Optional[str] = Field(secondary_index=True)
    c3: Optional[datetime]
    c4: Optional[Dict]
    c5: Optional[str]
    c6: Optional[X1]
    c7: Optional[Y1]


class AbstractModel(Model):

    _table = 'test_abstract_table'

    c1: str = Field(default='5', secondary_index=True)


class Next1Model(AbstractModel):

    c2: str = '6'


class Next2Model(AbstractModel):

    c3: str = '7'


class T2(Model):

    _table = 't2'

    t1: T1
    t11: Optional[T1]
