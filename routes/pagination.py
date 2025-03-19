from typing import TypeVar

from fastapi import FastAPI, Query
from fastapi_pagination import Page, paginate, add_pagination
from fastapi_pagination.customization import CustomizedPage, UseParamsFields

T = TypeVar("T")

LargePage = CustomizedPage[
    Page[T],
    UseParamsFields(
        size=Query(800, ge=1, le=1000),
    ),
]

__all__ = [LargePage]
