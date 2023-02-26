from functools import reduce
from typing import Any, Callable


def compose(*funcs: Callable[[Any], Any]) -> Callable[[Any], Any]:
    return reduce(lambda acc, cur: (lambda x: cur(acc(x))), funcs, lambda x: x)
