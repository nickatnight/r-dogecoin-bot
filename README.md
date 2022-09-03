# :dog: :space_invader: r-dogecoin-bot

A useless bot that fetches top meme posts from r/dogecoin which include 'Meme' flair. I shut [my](https://github.com/public-apis/public-apis/blob/master/README.md?plain=1#L1502) public api down in 2021, but decided to decouple the Reddit logic out of the api and into a stanalone library. Mostly using it to plug into [this](https://github.com/nickatnight/fastapi-backend-base) base project. Because....why not?

This bot was scaffolded with my [base reddit bot](https://github.com/nickatnight/docker-reddit-bot-base)

## Usage
Subclass database client `AbstractDbClient` and override it's abstract methods to interface with your db client(s)
```python
import asyncio

from asyncpraw import models
from r_dogecoin_bot.clients.database import AbstractDbClient
from r_dogecoin_bot.main import DogecoinMemeBot
from r_dogecoin_bot.types import RedditClientConfig

from my_db_session_config import async_session
from my_schema import MySchema


class PostgresSubmissionDbClient(AbstractDbClient[models.Submission, MySchema]):
    schema: MySchema = MySchema

    @classmethod
    async def process(cls, model: models.Submission) -> None:
        async with async_session() as session:
            my_model: MySchema = cls.schema(
                **{
                    "submission_title": model.title,
                    "submission_url": model.url,
                    "submission_id": model.id,
                    "permalink": model.permalink,
                    "author": model.author.name,
                    "created": model.created_utc,
                }
            )
            session.add(my_model)
            await session.commit()
            await session.refresh(my_model)

    @classmethod
    async def get_existing_ids(cls) -> List[str]:
        async with async_session() as session:
            result = await session.execute(
                select(cls.schema.submission_id)
            )
        return result.scalars().all()


class MongoSubmissionDbClient(AbstractDbClient[models.Submission, MySchema]):
    schema: MySchema = MySchema

    @classmethod
    async def process(cls, model: models.Submission) -> None:
        async with async_session() as session:
            data: MySchema = cls.schema(
                **{
                    "submission_title": model.title,
                    "submission_url": model.url,
                    "submission_id": model.id,
                    "permalink": model.permalink,
                    "author": model.author.name,
                    "created": model.created_utc,
                }
            )
            await session["myschema_collection"].insert_one(data.dict())

    @classmethod
    async def get_existing_ids(cls) -> List[str]:
        async with async_session() as session:
            result = await session["meme_collection"].distinct("submission_id")
        return result


async def main():
    reddit_config: RedditClientConfig = dict(
        client_id="much_client",
        client_secret="very_secret",
        user_agent="to_the_moon",
    )
    bot = DogecoinMemeBot(
        reddit_client_config=reddit_config,
        db_client=PostgresSubmissionDbClient,
    )

    await bot.run()


if __name__ == "__main__":
    asyncio.run(main())

```

## Development
Requires [Poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) to manage dev environment.  Once installed:
1. install packages with `poetry install`
2. black `poetry run black .`
3. flake8 `poetry run flake8`
4. test `poetry run pytest --cov=r_dogecoin_bot tests/`
5. build sdist `poetry build --format sdist`
6. create new setup.py
    ```shell
    $ tar -xvf dist/*-`poetry version -s`.tar.gz -O '*/setup.py' > setup.py
