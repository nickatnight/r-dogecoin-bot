# -*- coding: utf-8 -*-
from setuptools import setup


packages = ["r_dogecoin_bot", "r_dogecoin_bot.clients"]

package_data = {"": ["*"]}

install_requires = ["colorama>=0.4.4,<0.5.0", "emoji>=1.2.0,<2.0.0", "requests==2.28.1"]

entry_points = {"console_scripts": ["botnet = r_dogecoin_bot.main:main"]}

setup_kwargs = {
    "name": "r-dogecoin-bot",
    "version": "0.1.0",
    "description": "Top meme posts from r/dogecoin which include 'Meme' flair.",
    "long_description": "# :dog: :space_invader: docker-reddit-bot-base\n\nBot that fetches top meme posts from r/dogecoin which include 'Meme' flair. I shut [this](https://github.com/public-apis/public-apis/blob/master/README.md?plain=1#L1502) api down in 2021, but decided to decouple the Reddit logic out of the api and into a separate library. Mostly using it to plug into [this](https://github.com/nickatnight/fastapi-backend-base) base project. Because....why not?\n\n## Usage\nRequires [Poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) to manage dev environment.  Once installed:\n1. install packages with `poetry install`\n2. black `poetry run black .`\n3. flake8 `poetry run flake8`\n4. test `poetry run pytest --cov=r_dogecoin_bot tests/`\n5. build sdist `poetry build --format sdist`\n6. create new setup.py\n    ```shell\n    $ tar -xvf dist/*-`poetry version -s`.tar.gz -O '*/setup.py' > setup.py\n",
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
