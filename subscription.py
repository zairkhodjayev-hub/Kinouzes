from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from data.config import *
from database.base import *
from utils.helpful_functions import check_subscription
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from loader import bot

async def botisadminthischannel(username: str) -> bool:
    try:
        channel = await bot.get_chat(username)
        admins = await bot.get_chat_administrators(channel.id)
        return any(admin.user.id == bot.id for admin in admins)
    except Exception:
        return False
    
async def botisadminthischannelid(channelid: int) -> bool:
    try:
        admins = await bot.get_chat_administrators(channelid)
        return any(admin.user.id == bot.id for admin in admins)
    except Exception:
        return False    

async def generate_channel_buttons():
    try:
        channels = InlineKeyboardMarkup()
        channel_data = await find_channel_info()

        for channel_name, channel_username, channel_id in channel_data:
            if await botisadminthischannelid(channel_id):
                try:
                    channel_url = f"https://t.me/{channel_username}"
                    button = InlineKeyboardButton(text=channel_name, url=channel_url)
                    channels.add(button)
                except Exception:
                    pass

        button = InlineKeyboardButton(text="Tekshirish♻️", url=f"https://t.me/{BOTUSERNAME}?start=restart")
        channels.add(button)

        return channels
    except Exception:
        return None
    
import traceback

class CheckSubscriptionMiddleware(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        user_id = message.from_user.id
        CHANNEL_ID = await find_channel_ids()

        if not CHANNEL_ID:
            return

        if user_id not in ADMINS:
            for channel_id in CHANNEL_ID:
                if await botisadminthischannelid(channel_id):    
                    is_subscribed = await check_subscription(user_id, channel_id)
                    if not is_subscribed:
                        try:
                            response_text = "<b>Botdan foydalanish uchun kanalga a'zo bo'ling 👇</b>\n\n"
                            channels = await generate_channel_buttons()
                            await message.answer(response_text, reply_markup=channels)
                        except Exception:
                            pass
                        raise CancelHandler()