from typing import Hashable
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase


class BaseDeepCopyMixin:
    """Mixin to add deep_copy functionality to SQLAlchemy models."""

    def deep_copy[T](self: T, cache: dict[Hashable, DeclarativeBase] = None) -> T:
        return deep_copy(obj=self, cache=cache or {})


def make_cache_key(obj: DeclarativeBase) -> tuple:
    pk = [getattr(obj, k.key) for k in obj.__class__.__table__.c if k.primary_key]
    if any(pk_val is None for pk_val in pk):
        raise ValueError(f"Primary key(s) missing for object: {obj}")
    cache_key_pk = (obj.__class__.__name__, *pk)
    return cache_key_pk


def shallow_copy[T](obj: T) -> T:
    assert isinstance(obj, DeclarativeBase)
    class_ = obj.__class__
    kwargs = {
        k.key: getattr(obj, k.key)
        for k in class_.__table__.c
        if not k.primary_key and not k.foreign_keys
    }
    return class_(**kwargs)


def deep_copy[T](obj: T, cache: dict[Hashable, DeclarativeBase] = None) -> T:
    if obj is None:
        return None
    if cache is None:
        cache = {}
    assert isinstance(obj, DeclarativeBase)
    class_ = obj.__class__
    mapper = inspect(class_)

    cache_key_pk = make_cache_key(obj)
    if cached := cache.get(cache_key_pk, None):
        return cached

    new = shallow_copy(obj)

    # store parent before going down to children
    cache[cache_key_pk] = new

    for name, ref_ in mapper.relationships.items():
        refs = getattr(obj, name)
        deepcopied_refs = (
            [deep_copy(_, cache) for _ in refs]
            if isinstance(refs, list)
            else deep_copy(refs, cache)
        )
        if isinstance(refs, list):
            assert isinstance(refs, list) and isinstance(deepcopied_refs, list)
        setattr(new, name, deepcopied_refs)

    return new
