from fastapi_filter.contrib.sqlalchemy import Filter


class OapBaseFilter(Filter):
    order_by: list[str] | None = None
    program_id: int | None = None
    name: str | None = None
    name__in: list[str] | None = None
    id: int | None = None
    id__in: list[int] | None = None
