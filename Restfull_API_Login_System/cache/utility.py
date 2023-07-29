from datetime import timedelta
from .connection import client
from common.configuration import SETTINGS
SETTINGS = SETTINGS()
def get_data(key: str) -> str:
    try:
        """Get data from redis."""

        val = client.get(key)
    except:
        val = None

    return val



def set_data(key: str, value: str, seconds = SETTINGS.CACHE_EXPIRY_IN_SECONDS) -> bool:

    try:
        """Set data to redis."""

        state = client.setex(key, timedelta(seconds=seconds), value=value)
    except:
        state = False
    return state