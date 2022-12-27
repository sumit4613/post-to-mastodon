import os
import uuid
import logging
import requests

from src.constants import HTTPS_PREFIX, PORT_443, HTTP_PREFIX, POST_PATH

logger = logging.getLogger(__name__)

try:
    ACCESS_TOKEN = os.environ["access-token"]
except KeyError as e:
    raise ValueError("access-token is required") from e

HOST = os.environ["host"]
PORT = os.environ["port"]
API = os.environ["api"]
MESSAGE = os.environ["message"]
# TODO: support complex blog urls like https://www.example.com/blog/2020/01/01/first-post
BASE_BLOG_URL = os.environ["base-blog-url"]

PROTOCOL: str = HTTPS_PREFIX if PORT == PORT_443 else HTTP_PREFIX
BASE_URL: str = f"{PROTOCOL}{HOST}/{API}{POST_PATH}"


def post_to_mastodon():
    # https://docs.joinmastodon.org/methods/statuses/#headers
    headers: dict = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Idempotency-Key": str(uuid.uuid4()),
    }

    # https://docs.joinmastodon.org/methods/statuses/#form-data-parameters
    form_data: dict = {
        "status": f"{MESSAGE} \n\n {BASE_BLOG_URL}",
        "visibility": "public",
    }

    response = requests.post(BASE_URL, headers=headers, data=form_data)
    response.raise_for_status()


if __name__ == "__main__":
    logger.info("Posting to Mastodon")
    post_to_mastodon()
    logger.info("Posted to Mastodon")
