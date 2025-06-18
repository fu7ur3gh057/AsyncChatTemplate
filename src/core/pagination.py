from typing import Generic, TypeVar, List

from pydantic.generics import GenericModel

T = TypeVar("T")


class PaginatedResult(GenericModel, Generic[T]):
    total: int
    rows: int
    page: int
    items: List[T]
