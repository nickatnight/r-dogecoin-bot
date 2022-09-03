# -*- coding: utf-8 -*-
from setuptools import setup


packages = ["r_dogecoin_bot", "r_dogecoin_bot.clients"]

package_data = {"": ["*"]}

install_requires = ["asyncpraw>=7.5.0,<8.0.0"]

entry_points = {"console_scripts": ["botnet = r_dogecoin_bot.main:main"]}

setup_kwargs = {
    "name": "r-dogecoin-bot",
    "version": "0.1.4",
    "description": "Top meme posts from r/dogecoin which include 'Meme' flair.",
    "long_description": '# :dog: :space_invader: r-dogecoin-bot\n\nA useless bot that fetches top meme posts from r/dogecoin which include \'Meme\' flair. I shut [my](https://github.com/public-apis/public-apis/blob/master/README.md?plain=1#L1502) public api down in 2021, but decided to decouple the Reddit logic out of the api and into a stanalone library. Mostly using it to plug into [this](https://github.com/nickatnight/fastapi-backend-base) base project. Because....why not?\n\nThis bot was scaffolded with my [base reddit bot](https://github.com/nickatnight/docker-reddit-bot-base)\n\n## Usage\nSubclass database client `AbstractDbClient` and override it\'s abstract methods to interface with your db client(s)\n```python\nimport asyncio\n\nfrom asyncpraw import models\nfrom r_dogecoin_bot.clients.database import AbstractDbClient\nfrom r_dogecoin_bot.main import DogecoinMemeBot\nfrom r_dogecoin_bot.types import RedditClientConfig\n\nfrom my_db_session_config import async_session\nfrom my_schema import MySchema\n\n\nclass PostgresSubmissionDbClient(AbstractDbClient[models.Submission, MySchema]):\n    schema: MySchema = MySchema\n\n    @classmethod\n    async def process(cls, model: models.Submission) -> None:\n        async with async_session() as session:\n            my_model: MySchema = cls.schema(\n                **{\n                    "submission_title": model.title,\n                    "submission_url": model.url,\n                    "submission_id": model.id,\n                    "permalink": model.permalink,\n                    "author": model.author.name,\n                    "created": model.created_utc,\n                }\n            )\n            session.add(my_model)\n            await session.commit()\n            await session.refresh(my_model)\n\n    @classmethod\n    async def get_existing_ids(cls) -> List[str]:\n        async with async_session() as session:\n            result = await session.execute(\n                select(cls.schema.submission_id)\n            )\n        return result.scalars().all()\n\n\nclass MongoSubmissionDbClient(AbstractDbClient[models.Submission, MySchema]):\n    schema: MySchema = MySchema\n\n    @classmethod\n    async def process(cls, model: models.Submission) -> None:\n        async with async_session() as session:\n            data: MySchema = cls.schema(\n                **{\n                    "submission_title": model.title,\n                    "submission_url": model.url,\n                    "submission_id": model.id,\n                    "permalink": model.permalink,\n                    "author": model.author.name,\n                    "created": model.created_utc,\n                }\n            )\n            await session["myschema_collection"].insert_one(data.dict())\n\n    @classmethod\n    async def get_existing_ids(cls) -> List[str]:\n        async with async_session() as session:\n            result = await session["meme_collection"].distinct("submission_id")\n        return result\n\n\nasync def main():\n    reddit_config: RedditClientConfig = dict(\n        client_id="much_client",\n        client_secret="very_secret",\n        user_agent="to_the_moon",\n    )\n    bot = DogecoinMemeBot(\n        reddit_client_config=reddit_config,\n        db_client=PostgresSubmissionDbClient,\n    )\n\n    await bot.run()\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n\n```\n\n## Development\nRequires [Poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) to manage dev environment.  Once installed:\n1. install packages with `poetry install`\n2. black `poetry run black .`\n3. flake8 `poetry run flake8`\n4. test `poetry run pytest --cov=r_dogecoin_bot tests/`\n5. build sdist `poetry build --format sdist`\n6. create new setup.py\n    ```shell\n    $ tar -xvf dist/*-`poetry version -s`.tar.gz -O \'*/setup.py\' > setup.py\n',
    "author": "nickatnight",
    "author_email": "nickkelly.858@gmail.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://github.com/nickatnight/r-dogecoin-bot",
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.9,<4.0",
}


setup(**setup_kwargs)
