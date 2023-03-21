import os
import string
import asyncio
import requests
from mdisky import Mdisk

from pyrogram import Client, filters, enums


BOT_TOKEN = os.environ.get("BOT_TOKEN", "5082443380:AAHrI25NGvbdr6cRXJfiwq2a1iiargGKqwE")

API_ID = int(os.environ.get("API_ID", "2276460"))

API_HASH = os.environ.get("API_HASH", "1ee636feaecb523f12c844416dda70e3")

API_KEY = os.environ.get("API_KEY", "tHRFNVu8CkjkdstzXNsp")

app = Client("tgid", bot_token=BOT_TOKEN, api_hash=API_HASH, api_id=API_ID)


@Client.on_message(filters.command(['start']))
async def start(client, message):
    await message.reply_text(text=f"Hello 👋\n\nI'm a telegram bot which convert MDisk link to your Link", reply_to_message_id=message.message_id)


@Client.on_message(filters.command(['mdisk']))
async def mdisk(client, message):
    await app.send_chat_action(chat_id, enums.ChatAction.TYPING)
    
    mt = message.text
    if (" " in message.text):
        cmd, url = message.text.split(" ", 1)
    caption = await get_caption(message.from_user.id)
    caption_text = caption.caption
    API_KEY = caption_text
    mdisk = Mdisk(API_KEY)
    link = await mdisk.convert(url)
    await message.reply_text(text=f"{link}")
    print(link)


@Client.on_message(filters.command(['rename']))
async def rename(client, message):
    mt = message.text
    if (" " in message.text):
        cmd, txt = message.text.split(" ", 1)
    if ("|" in txt):
        url_parts = txt.split("|")
        if len(url_parts) == 2:
            url = url_parts[0]
            file_name = url_parts[1]
    caption = await get_caption(message.from_user.id)
    caption_text = caption.caption
    API_KEY = caption_text
    mdisk = Mdisk(API_KEY)
    link = await mdisk.change_filename(url, file_name)
    await message.reply_text(text=f"**New Filename:** {file_name}\n\n**URL:** {url}")
    print(link)


@Client.on_message(filters.command(['filename']))
async def filename(client, message):
    mt = message.text
    if (" " in message.text):
        cmd, url = message.text.split(" ", 1)
    caption = await get_caption(message.from_user.id)
    caption_text = caption.caption
    API_KEY = caption_text
    mdisk = Mdisk(API_KEY)
    filename = await mdisk.get_filename(url)
    await message.reply_text(text=f"**Filename:** {filename}")
    print(filename)


@Client.on_message(filters.command(['auth']))
async def set_caption(client, message):
    if len(message.command) == 1:
        await message.reply_text(
            "Use this command to set your own Mdisk Api Key \n\nEg:- `/auth your mdisk key`", 
            quote = True
        )
    else:
        command, caption = message.text.split(' ', 1)
        await update_caption(message.from_user.id, caption)
        await message.reply_text(f"__Authorised Successfully__", quote=True)


@Client.on_message(filters.command(['me']))
async def view_caption(client, message):
    if (message is not None):
        try:
            caption = await get_caption(message.from_user.id)
            caption_text = caption.caption
        except:
            caption_text = "Not Authorised" 
        await message.reply_text(
            f"API KEY: {caption_text}",
            quote = True
        )


@Client.on_message(filters.command(['unauth']))
async def view_caption(client, message):
    if (message is not None):
        try:
            caption = await del_caption(message.from_user.id)
        except:
            caption_text = "Not Authorised me" 
        await message.reply_text(
            "Unauthorised successfully",
            quote = True
        )



