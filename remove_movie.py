from aiogram import types
from aiogram.types import CallbackQuery, ContentType
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from keyboards.inline.keyrboards import adminmenu, cancel
from states.state import *
from filters.adminchecker import IsAdmin
from data.config import *
from database.base import *
from aiogram.types import ReplyKeyboardRemove

@dp.callback_query_handler(text="remove_movie")
async def remove_movie(callback_query: CallbackQuery):
    await callback_query.message.answer("🎬 Kino kodini jo'nating:", reply_markup=cancel)
    await detelemovie.moviecode.set()

@dp.message_handler(state=detelemovie.moviecode)
async def process_remove_movie(message: types.Message, state: FSMContext):         
    code = message.text
    await deletemoviebot(code)
    await message.answer("✅ Kino botdan o'chirildi!", reply_markup=adminmenu)
    await state.finish()
