import typing

K = typing.TypeVar("K")
V = typing.TypeVar("V")

class keydefaultdict(dict[K, V]):
    default_factory: typing.Callable[[K], V] | None
    def __init__(self, default_factory, *args, **kwargs):
        self.default_factory = default_factory
        super().__init__(*args, **kwargs)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError( key )
        else:
            ret = self[key] = self.default_factory(key)
            return ret
