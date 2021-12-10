# (c) https://t.me/Mr_Robot_t

from core.login import doodstream_login

DOODSTREAM_DB = {}


async def get_cookies(username: str, password: str) -> str:
    if not DOODSTREAM_DB:
        user_id, cookies = await doodstream_login(username, password)
        DOODSTREAM_DB["cookies"] = cookies
        DOODSTREAM_DB["user_id"] = user_id
        DOODSTREAM_DB["username"] = username
        DOODSTREAM_DB["password"] = password

    return DOODSTREAM_DB["cookies"]


async def set_cookies(data: dict):
    DOODSTREAM_DB["username"] = data["username"]
    DOODSTREAM_DB["password"] = data["password"]
    DOODSTREAM_DB["user_id"] = data["user_id"]
    DOODSTREAM_DB["cookies"] = data["cookies"]
