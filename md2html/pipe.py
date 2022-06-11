from typing import Callable, TypeVar

T = TypeVar("T")


def pipe(value: T, *args: Callable[[T], T]) -> T:
    acc = value

    for f in args:
        acc = f(acc)

    return acc
