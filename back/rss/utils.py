
from urllib.parse import urlparse


def is_abs_url(url: str):
    return bool(urlparse(url).netloc)
