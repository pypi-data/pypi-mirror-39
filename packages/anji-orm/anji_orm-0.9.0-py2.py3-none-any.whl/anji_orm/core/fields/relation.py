import asyncio
import functools
import operator
from typing import Type, TYPE_CHECKING, Union

from toolz import itertoolz

from .base import Field
from ..register import orm_register


if TYPE_CHECKING:
    from ..model import Model  # pylint: disable=unused-import

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.9.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"

__all__ = ['LinkField']


def set_to_cache(model_class, model_id, result):
    if isinstance(result, asyncio.Future):
        result = result.result()
    orm_register.shared.relation_cache[model_class._table][model_id] = result


def get_model_and_load_to_cache(model_class, model_id):
    if orm_register.async_mode:
        result: asyncio.Task = asyncio.ensure_future(model_class.async_get(model_id))
        result.add_done_callback(functools.partial(set_to_cache, model_class, model_id))
    else:
        result = model_class.get(model_id)
        set_to_cache(model_class, model_id, result)
    return result


class LinkField(Field):

    def __init__(
            self, **kwargs) -> None:
        """
        """
        super().__init__(**kwargs)
        self._table_name: str
        self._model_class: Type['Model']
        self._allow_none: bool = False

    # pylint: disable=no-member
    @Field.param_type.setter  # type: ignore
    def param_type(self, value: Type['Model']) -> None:
        self._param_type = value
        self._model_class = value
        if hasattr(self._model_class, '__origin__'):
            if self._model_class.__origin__ is Union:  # type: ignore
                self._allow_none = itertoolz.count(filter(lambda x: isinstance(None, x), self._model_class.__args__)) > 0  # type: ignore
                self._model_class = itertoolz.first(filter(operator.truth, self._model_class.__args__))  # type: ignore
        self._table_name = self._model_class._table

    def real_value(self, model_record):
        return model_record._values.get(self.name)

    def can_be(self, target_type: Type) -> bool:
        if issubclass(str, target_type):
            return True
        return super().can_be(target_type)

    def __set__(self, instance, value) -> None:
        if not (isinstance(value, str) or (value is None and self._allow_none)):
            raise ValueError(f'Field {self.name} value should have by valid database id instead of {value}')
        instance._values[self.name] = orm_register.backend_adapter.ensure_compatibility(value)

    def __get__(self, instance, instance_type):
        if instance is None:
            return self._get_query_row_for_type(instance_type)
        model_id = instance._values.get(self.name)
        result = orm_register.shared.relation_cache[self._table_name].get(model_id)
        if result is None:
            if model_id is not None:
                result = get_model_and_load_to_cache(self._model_class, model_id)
        return result


# class LinkListField(Field):

#     def __init__(self, model_class, **kwargs) -> None:
#         super().__init__(
#             list,
#             description=model_class.__doc__,
#             default=None,
#             **kwargs
#         )
#         self._model_class = model_class
#         self._table_name = model_class._table
#         self._table = R.table(model_class._table)
#         self._created_list: List = []

#     def _fetch_from_model_list(self, instance) -> List[str]:
#         value_ids = [x.id for x in self._created_list]
#         instance._values[self.name] = value_ids
#         return value_ids

#     def real_value(self, model_record):
#         if self._created_list is not None:
#             return self._fetch_from_model_list(model_record)
#         return model_record._values[self.name]

#     def __get__(self, instance, instance_type):
#         if instance is None:
#             return self._get_query_row_for_type(instance_type)
#         if self._created_list is None:
#             self._created_list = []
#             model_ids = instance._values.get(self.name)
#             if model_ids:
#                 for model_id in model_ids:
#                     result = instance.shared.relation_cache[self._table_name].get(model_id)
#                     if result is None:
#                         if model_id is not None:
#                             result = get_model_and_load_to_cache(self._model_class, instance, model_id)
#                     self._created_list.append(result)
#         return self._created_list

#     def __set__(self, instance, value) -> None:
#         if value is not None and not isinstance(value, self.param_type):
#             raise ValueError(f'Field {self.name} value should have {str(self.param_type)} type instead of {value}')
#         if value:
#             for value_record in value:
#                 if not isinstance(value_record, (self._model_class, asyncio.Future, str)):
#                     raise ValueError(f"This field only for model for {self._model_class}")
#         # None value should be converted to empty list
#         if self._created_list is not None:
#             self._created_list.clear()
#         if not value:
#             self._created_list = []
#             instance._values[self.name] = []
#         elif isinstance(value[0], str):
#             self._created_list = None
#             instance._values[self.name] = value
#         else:
#             self._created_list = value
#             self._fetch_from_model_list(instance)
