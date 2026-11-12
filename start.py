from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import *
from aiogram.types import ParseMode
from loader import dp,bot
from keyboards.inline.keyrboards import *
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.types import CallbackQuery
from database.base import save_each_table_to_excel,adduser


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await adduser(message.from_user.full_name,message.from_user.username,message.from_user.id)
    await message.answer(f"""👋 Assalomu aleykum {message.from_user.full_name}!

🍿 Botimiz orqali siz o‘zingizga kerakli kinoni yuklab ko‘rishingiz mumkin.

<b><blockquote>
📊 Bot buyruqlari:
/start - Botni yangilash ♻️
/dev - Bot dasturchisi 👨‍💻
</blockquote></b>                                 
#️⃣ Kinoni kod orqali yuklashingiz ham mumkin. Marhamat, kino kodini yuboring:""",reply_markup=FILMSDATABUTTON)





@dp.message_handler(commands=['dev'])
async def send_films(message: types.Message):
    await message.answer(f"<b><a href='{devv}'>Dasturchining to'liq ma'lumoti uchun bosing!</a></b>", parse_mode=ParseMode.HTML)


@dp.message_handler(text="🛠️ Bakor qilish",state="*")
async def handle_bakor(message: types.Message, state: FSMContext):
    await state.finish()
    if message.from_user.id in ADMINS:
        await message.answer(f"Kino kodini kiriting... 🎬", reply_markup=adminmenu)
    else:
        await message.answer(f"Kino kodini kiriting... 🎬", reply_markup=ReplyKeyboardRemove())

@dp.callback_query_handler(text="backup",state="*")
async def handle_bakor(callback_query: CallbackQuery, state: FSMContext):
    await state.finish()
    if callback_query.from_user.id in ADMINS:
        await callback_query.message.answer(
            "Kino kodini kiriting... 🎬", 
            reply_markup=adminmenu
        )
    else:
        await callback_query.message.answer(
            "Siz bu amallarni bajarish huquqiga ega emassiz! ❌", 
            reply_markup=ReplyKeyboardRemove()
        )
