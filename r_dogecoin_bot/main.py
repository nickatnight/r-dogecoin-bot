#!/usr/bin/env python3

import asyncio
import copy
from typing import List, Optional

import asyncpraw
from aiohttp import ClientSession
from fastapi.logger import logger

from r_dogecoin_bot.clients.database import AbstractDbClient
from r_dogecoin_bot.types import RedditClientConfig


default_user_agent = "botnet| v1 | By nickatnight"


class DogecoinMemeBot:
    """much meme, very api"""

    def __init__(
        self, reddit_client_config: RedditClientConfig, db_client: Optional[AbstractDbClient]
    ):
        self.reddit_client_config = reddit_client_config
        self.db_client = db_client

        logger.info(
            f"Starting up... {self.reddit_client_config.get('user_agent') or default_user_agent}"
        )

    async def run(self):
        sub_ids: List[str] = self.db_client.get_existing_ids()
        config_data: RedditClientConfig = copy.deepcopy(self.reddit_client_config)

        async with ClientSession(trust_env=True) as session:
            config_data.update(requestor_kwargs={"session": session})

            async with asyncpraw.Reddit(**config_data) as reddit:
                subreddit: asyncpraw.models.Subreddit = await reddit.subreddit("dogecoin")

                async for submission in subreddit.hot():
                    skip: bool = submission.id in sub_ids or submission.link_flair_text != "Meme"

                    if not skip:
                        if getattr(self, "db_client"):
                            await self.db_client.process(submission)


async def main():
    b = DogecoinMemeBot()
    await b.run()


if __name__ == "__main__":
    asyncio.run(main())
