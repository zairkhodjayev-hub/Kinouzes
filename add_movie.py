from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from keyboards.inline.keyrboards import adminmenu, cancel,bot_channel,trailer_keyboard
from states.state import *
from filters.adminchecker import IsAdmin
from data.config import *
from database.base import *
from aiogram.types import ReplyKeyboardRemove


@dp.callback_query_handler(IsAdmin(),text="add_movie")
async def add_movie(callback_query: CallbackQuery):
    await callback_query.message.answer("📹 Kinoni jo'nating:", reply_markup=cancel)
    await addmoviestate.Video.set()

@dp.message_handler(state=addmoviestate.Video, content_types=ContentType.VIDEO)
async def process_video(message: types.Message, state: FSMContext):
    video = message.video
    file_id = video.file_id
    await message.answer("✅ Video qabul qilindi. Tavsifni kiriting:")
    await message.answer("""📝 Text shablon:\n\n`
🎥 Nomi: 
📹 Sifati: 
📆 Yili: 
🎞 Janri: 
🇺🇸 Davlati: 
🇺🇿 Tili: 
`""", parse_mode=types.ParseMode.MARKDOWN)
    await state.update_data(Video=file_id)
    await addmoviestate.VideoCaption.set()

@dp.message_handler(state=addmoviestate.Video)
async def process_invalid_video(message: types.Message, state: FSMContext):
    await message.answer("⚠️ Iltimos, videoni faqat video qilib kiritish kerak.")

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@dp.message_handler(state=addmoviestate.VideoCaption)
async def process_caption(message: types.Message, state: FSMContext):
    code = await generate_unique_movie_code()
    text = f"""
{message.text}

📔Code: `{code}`

"""
    await state.update_data(VideoCaption=text)
    video = (await state.get_data()).get('Video')
    caption = (await state.get_data()).get('VideoCaption')
    newcaption = f"{caption}\n0Hoziroq tomosha qiling👀"
    await addmoviebot(str(video), str(caption), str(code))
    await message.answer(f"Kino botga qo'shildi! Kodi>> {code}\nESINGIZDA BO'LSIN,HOZIR KINO KO'DINI JO'NATMANG,HOZIR TUGMALARDAN BIRINI BOSING,KINO TO'LIQ QO'SHILGANDAN SO'NG KINO KODINI TASHLAB TEST QILASIZ\n\n🎥 Trailer mavjudmi?", reply_markup=trailer_keyboard)
    await addmoviestate.Trailer.set()

@dp.callback_query_handler(state=addmoviestate.Trailer, text="add_trailer")
async def add_trailer(callback_query: CallbackQuery):
    await callback_query.message.answer("📹 Trailerni jo'nating:", reply_markup=cancel)
    await addmoviestate.TrailerVideo.set()

@dp.message_handler(state=addmoviestate.TrailerVideo, content_types=ContentType.VIDEO)
async def process_trailer(message: types.Message, state: FSMContext):
    trailer = message.video.file_id
    video = (await state.get_data()).get('Video')
    caption = (await state.get_data()).get('VideoCaption')
    trailer_caption = f"{caption}\n🎥 Trailer:"
    try:
        await bot.send_video(chat_id=FILMSDATAID, video=trailer, caption=trailer_caption, parse_mode=types.ParseMode.MARKDOWN, reply_markup=bot_channel)
        await state.finish()
        await message.answer("✅ Kino va trailer muvaffaqiyatli qo'shildi!", reply_markup=adminmenu)

    except:
        await state.finish()
        await message.answer("✅ Kino va trailer muvaffaqiyatli qo'shildi! Ammo kanalga jo'natishda hatolik ketdi!", reply_markup=adminmenu)


@dp.callback_query_handler(state=addmoviestate.Trailer, text="no_trailer")
async def no_trailer(callback_query: CallbackQuery, state: FSMContext):
    video = (await state.get_data()).get('Video')
    caption = (await state.get_data()).get('VideoCaption')
    try:
        await bot.send_message(chat_id=FILMSDATAID, text=caption, parse_mode=types.ParseMode.MARKDOWN, reply_markup=bot_channel)
        await state.finish()
        await callback_query.message.answer("✅ Kino muvaffaqiyatli qo'shildi!", reply_markup=adminmenu)
    except:
        await bot.send_message(chat_id=FILMSDATAID, text=caption, parse_mode=types.ParseMode.MARKDOWN, reply_markup=bot_channel)
        await state.finish()
        await callback_query.message.answer("✅ Kino muvaffaqiyatli qo'shildi! Ammo kanalga tashashda muammo bo'ldi!", reply_markup=adminmenu)
