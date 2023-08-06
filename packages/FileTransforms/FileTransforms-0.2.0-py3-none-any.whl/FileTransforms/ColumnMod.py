from typing import Any, Callable


class ColumnMod:

    def __init__(self, prefix=None, suffix=None, func: Callable[[Any], Any]=None):
        self.prefix = prefix
        self.suffix = suffix
        self.func = func

    def apply(self, v):
        ret = self.func(v) if self.func is not None else v

        if self.prefix:
            ret = str(self.prefix) + str(ret)

        if self.suffix:
            ret = str(ret) + str(self.suffix)

        return ret
