import datetime
import pytz
from typing import Callable, TypeVar, List, Tuple, Dict
from decorator import decorate

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')


def utcnow() -> datetime.datetime:
    return datetime.datetime.utcnow().replace(tzinfo=pytz.UTC)


def gen_to_list(f: Callable[[A], B]) -> Callable[[A], List[B]]:
    def _g_to_l(gen, *args, **kwargs) -> list:
        return list(gen(*args, **kwargs))

    return decorate(f, _g_to_l)


def gen_to_tuple(f: Callable[[A], B]) -> Callable[[A], Tuple[B]]:
    def _g_to_l(gen, *args, **kwargs) -> Tuple:
        return tuple(gen(*args, **kwargs))

    return decorate(f, _g_to_l)


def gen_to_dict(f: Callable[[A], Tuple[B, C]]) -> Callable[[A], Dict[B, C]]:
    def _g_to_d(gen, *args, **kwargs) -> dict:
        return {k: v for (k, v) in gen(*args, **kwargs)}

    return decorate(f, _g_to_d)
