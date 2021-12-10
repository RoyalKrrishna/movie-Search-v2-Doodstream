
import os
import asyncio
import traceback
from dotenv import (
    load_dotenv
)
from pyrogram import (
    Client,
    filters,
    idle
)
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from pyrogram.errors import (
    MessageNotModified
)
from core.search_video import search_doodstream_videos

if os.path.exists("configs.env"):
    load_dotenv("configs.env")


class Configs(object):
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    DOODSTREAM_USERNAME = os.environ.get("DOODSTREAM_USERNAME", "")
    DOODSTREAM_PASSWORD = os.environ.get("DOODSTREAM_PASSWORD", "")
    MAX_RESULTS = int(os.environ.get("MAX_RESULTS", 5))
    # Which DOODSTREAM Domain?
    PDISK_DOMAINS = [
        "https://doodstream.com/",
        
      
    ]
    DOODSTREAM_DOMAIN = os.environ.get("DOODSTREAM_DOMAIN", DOODSTREAM_DOMAINS[2])


DoodstreamBot = Client(
    session_name=":memory:",
    api_id=Configs.API_ID,
    api_hash=Configs.API_HASH,
    bot_token=Configs.BOT_TOKEN
)


@DoodstreamBot.on_message(filters.command("start") & ~filters.edited)
async def start_handler(_, m: Message):
    await m.reply_text("**Hey**🙏🏻 \n\n I am a Pdisk Movie Searcher Bot.\n\n✅**Send me any movie name i will give you pdisk link**\n\n ", quote=True,
                      reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton("For help", url="https://t.me/ALL_WEB_SERIESSS_REQUEST_BOT")]
                                 ]))
    
    
@DoodstreamBot.on_message( ~filters.edited, group=-1)
async def text_handler(_, m: Message):
    editable = await m.reply_text("**Searching 🔎 Your Movie\n Please Wait...⏳⏳**\n\n**✅For Help - @ALL_WEB_SERIESSS_REQUEST_BOT** ", quote=True,
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton("For Any help contact", url="https://t.me/ALL_WEB_SERIESSS_REQUEST_BOT")]
                                 ]))
    response = await search_doodstream_videos(m.text.split(" ", 1)[-1], Configs.DOODSTREAM_USERNAME, Configs.DOODSTREAM_PASSWORD)
    if isinstance(response, Exception):
        traceback.print_exc()
        try: await editable.edit("Failed to search!",
                                 reply_markup=InlineKeyboardMarkup([
                                     [InlineKeyboardButton("Request movie", url="https://t.me/ALL_WEB_SERIESSS_REQUEST_BOT")]
                                 ]))
        except MessageNotModified: pass
    elif not response["data"]["list"]:
        try: await editable.edit("**If Movie Not Available then -  **🥺\n\n **Request Here - @ALL_WEB_SERIESSS_REQUEST_BOT**\n")
        except MessageNotModified: pass
    else:
        data = response["data"]["list"]
        text = ""
        count = 0
        for i in range(len(data)):
            if count > Configs.MAX_RESULTS:
                break
            count += 1
            text += f"**♻️ Title: `{data[i]['title']}`\n**" \
                    f"**⚡️ Link:** {Configs.DOODSTREAM_DOMAIN + 'share-video?videoid=' + data[i]['share_link'].split('=', 1)[-1]}\n\n\n"
        try: await editable.edit(text, disable_web_page_preview=True)
        except MessageNotModified: pass


async def run():
    await DoodstreamBot.start()
    print("\n\nBot Started!\n\n")
    await idle()
    await DoodstreamBot.stop()
    print("\n\nBot Stopped!\n\n")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
