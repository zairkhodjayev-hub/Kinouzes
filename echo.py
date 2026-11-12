from aiogram import types
from aiogram.types import ReplyKeyboardRemove 
from loader import dp, bot
from keyboards.inline.keyrboards import FILMSDATABUTTON
from data.config import *
from database.base import *

@dp.message_handler()
async def start_handler(message: types.Message):
    try:
        code = message.text
        movie = await findmovie(code)
        video_id_or_url = movie[0]
        caption = movie[1]
        if movie:
            await bot.send_video(video=video_id_or_url, caption=caption, chat_id=message.chat.id)
        else:
            await message.answer(f"🎬 Kino topilmadi! 😞📺",reply_markup=FILMSDATABUTTON)
    except:
        await message.answer(f"🎬 Kino topilmadi! 😞📺",reply_markup=FILMSDATABUTTON)

