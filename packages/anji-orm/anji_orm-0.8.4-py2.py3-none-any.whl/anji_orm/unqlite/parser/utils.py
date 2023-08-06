import typing

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.8.4"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"
__all__ = ['UnqliteQuery']


class UnqliteQuery:

    __slots__ = (
        'table', 'filter_function',
        'post_hooks', 'pre_hooks'
    )

    def __init__(self, table: str) -> None:
        self.table = table
        self.filter_function: typing.Optional[typing.Callable[[typing.Any], bool]] = None
        self.post_hooks: typing.List[typing.Callable[[typing.Any], typing.Any]] = []
        self.pre_hooks: typing.List[typing.Callable[[typing.Any], typing.Any]] = []

    def add_post_hook(self, hook: typing.Callable[[typing.Any], typing.Any]) -> None:
        self.post_hooks.append(hook)

    def add_pre_hook(self, hook: typing.Callable[[typing.Any], typing.Any]) -> None:
        self.pre_hooks.append(hook)

    def set_filter(self, filter_function: typing.Callable[[typing.Any], bool]) -> None:
        self.filter_function = filter_function
