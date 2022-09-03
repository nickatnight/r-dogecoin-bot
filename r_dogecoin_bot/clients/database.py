import abc
from typing import Generic, List, TypeVar


RedditType = TypeVar("RedditType")
SchemaType = TypeVar("SchemaType")


class AbstractDbClient(Generic[RedditType, SchemaType], abc.ABC):
    schema: SchemaType

    @classmethod
    @abc.abstractmethod
    async def process(cls, model: RedditType) -> None:
        ...

    @classmethod
    @abc.abstractmethod
    async def get_existing_ids(cls) -> List[str]:
        ...
