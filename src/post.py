import logging
import os
import uuid

import requests

from constants import Protocol, PORT_443, POST_PATH, PUBLISH_STR, Signs

logger = logging.getLogger(__name__)

try:
    ACCESS_TOKEN = os.environ["access-token"]
except KeyError as e:
    raise ValueError("access-token is required") from e

HOST = os.environ["host"]
PORT = os.environ["port"]
API = os.environ["api"]
MESSAGE = os.environ["message"]
BASE_DIRECTORY_NAME: str = os.environ["base-directory"]
# TODO: support complex blog urls like https://www.example.com/blog/2020/01/01/first-post
BASE_BLOG_URL = os.environ["base-blog-url"]

PROTOCOL: str = Protocol.HTTPS if PORT == PORT_443 else Protocol.HTTP
BASE_URL: str = f"{PROTOCOL}{HOST}/{API}{POST_PATH}"

COMMIT_MESSAGE_WITH_FILE_NAMES: str = os.environ["RECENTLY_ADDED_FILES"]


def parse_commit_message(commit_message_with_file_names: str) -> str:
    message_strings = commit_message_with_file_names.split(Signs.PIPE)
    for strings in message_strings:
        stripped_string = strings.strip()
        if stripped_string.startswith(BASE_DIRECTORY_NAME):
            # eg: "content/posts/python-decorators.md"
            # I'm returning the first file name that matches the base directory name
            # I'm assuming that the file name will be the same as the url slug
            # TODO: maybe make it more generic
            return stripped_string.split(Signs.FORWARD_SLASH)[-1].split(".")[0]


def post_to_mastodon(url_slug_: str) -> None:
    # https://docs.joinmastodon.org/methods/statuses/#headers
    headers: dict = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Idempotency-Key": str(uuid.uuid4()),
    }

    # https://docs.joinmastodon.org/methods/statuses/#form-data-parameters
    form_data: dict = {
        "status": f"{MESSAGE} \n\n {BASE_BLOG_URL}{url_slug_}",
        "visibility": "public",
    }

    response = requests.post(BASE_URL, headers=headers, data=form_data)
    response.raise_for_status()


if __name__ == "__main__":
    if PUBLISH_STR in COMMIT_MESSAGE_WITH_FILE_NAMES:
        logger.info("Parsing commit message and getting the url slug")
        if url_slug := parse_commit_message(COMMIT_MESSAGE_WITH_FILE_NAMES):
            logger.info("Posting to Mastodon")
            post_to_mastodon(url_slug)
            logger.info("Posted to Mastodon")
        else:
            logger.info("No url slug found in commit message. Skipped posting to Mastodon")

    else:
        logger.info("No new files to post")
