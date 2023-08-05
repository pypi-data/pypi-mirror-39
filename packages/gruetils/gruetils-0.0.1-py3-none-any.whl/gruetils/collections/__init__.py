import typing
from collections import defaultdict


class KeyedDefaultDict(defaultdict):
    def __missing__(self, key: typing.Hashable) -> typing.Any:
        if self.default_factory is None:
            raise KeyError(key)
        return self.default_factory(key)
