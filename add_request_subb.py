from aiogram import types
from loader import dp,bot
from aiogram.dispatcher import FSMContext
from filters.adminchecker import IsAdmin
from keyboards.inline.keyrboards import adminmenu
from aiogram.types import CallbackQuery
from database.base import *
from keyboards.inline.keyrboards import *
from data.config import *
from aiogram.types import ReplyKeyboardRemove
from states.state import *
import re


def extract_username(url: str) -> str:
    return re.sub(r"https://t.me/", "", url)

@dp.callback_query_handler(IsAdmin(),text="add_subscription_r")
async def add_channel(callback_query: CallbackQuery):
    if callback_query.from_user.id in ADMINS:
        conn, cur = await connect_db()
        cur.execute("SELECT ChannelName, Channelusername, Channelid FROM Channels")
        all_channels = cur.fetchall()
        conn.close()

        if all_channels:
            channel_info = "📋 Barcha majburiy kanallar:\n"
            for channel in all_channels:
                if len(channel) == 3:
                    try:
                        channel_name, channel_username, channel_id = channel
                        channel_info += f"📝 Kanal nomi: {channel_name}\n" \
                                        f"🔗 Kanal username: @{channel_username}\n" \
                                        f"🆔 Kanal ID: {channel_id}\n\n"
                    except ValueError as e:
                        print(f"Error unpacking channel data: {e}")
                        channel_info += "🚫 Kanal ma'lumotlarida xatolik.\n"
                else:
                    channel_info += "🚫 Kanal ma'lumotlarida xato: noto'g'ri tuzilma.\n"
            await callback_query.message.answer(channel_info)
            await callback_query.message.answer(
                "📑 Obuna bo'lish majburiy bo'lgan kanalni qo'shish uchun nimalar kerakligini o'qib chiqing:\n\n"
                "📌 Kanal nomi\n📌 Kanalning linki\n📌 Kanalning idsi\n\n"
                "⚠️ Bot majburiy obuna qo'shilgan telegram kanalda admin bo'lishi kerak."
            )
            await callback_query.message.answer(
                "Agar barchasi tayyor bo'lsa kanalning nomini kiriting:", 
                reply_markup=cancel
            )
            await addchannelr.name.set()
        else:
            await callback_query.message.answer("🚫 Hozirda kanallar mavjud emas.")
            await callback_query.message.answer(
                "📑 Obuna bo'lish majburiy bo'lgan kanalni qo'shish uchun nimalar kerakligini o'qib chiqing:\n\n"
                "📌 Kanal nomi\n📌 Kanalning linki\n📌 Kanalning idsi\n\n"
                "⚠️ Bot majburiy obuna qo'shilgan telegram kanalda admin bo'lishi kerak."
            )
            await callback_query.message.answer(
                "Agar barchasi tayyor bo'lsa kanalning nomini kiriting:", 
                reply_markup=cancel
            )
            await addchannelr.name.set()
    else:
        await callback_query.message.reply(
            "🚫 Admin huquqlari sizda yo'q", 
            reply_markup=ReplyKeyboardRemove()
        )
    await callback_query.answer()

@dp.message_handler(state=addchannelr.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    await state.update_data(name=name)
    await message.answer(
        "✅ Kanal nomi tayyor bo'ldi.\n📲 Kanalning linkiri jo'nating:\n\n(Iltimos kanal linki request jo'natadigan link bo'lsin,bo'lmasa hatolik yuz berishi mumkin!)",
        reply_markup=cancel
    )
    await addchannelr.username.set()

@dp.message_handler(state=addchannelr.username)
async def process_username(message: types.Message, state: FSMContext):
    try:
        username = extract_username(message.text)
    except:
        username = message.text
    if username.startswith("@"):
        await message.answer("⚠️ Iltimos, usernamesni @ ishlatmasdan kiriting.")
        return
    await state.update_data(username=username)
    await message.answer(
        "✅ Kanal link tayyor bo'ldi.\n🆔 Kanalning ID sini kiriting:",
        reply_markup=cancel
    )
    await addchannelr.channelid.set()

@dp.message_handler(state=addchannelr.channelid)
async def process_channelid(message: types.Message, state: FSMContext):
    try:
        channelid = int(message.text.strip())
        try:
            await bot.send_message(chat_id=channelid, text="✅ Bot kanalga ulandi.")
        except Exception as e:
            await message.answer(
                "⚠️ Kanal ID noto'g'ri yoki bot kanalga admin qilib qo'shilmagan.\nIltimos, tekshirib qaytadan kiriting."
            )
            return
        
        data = await state.get_data()
        name = data.get('name')
        username = data.get('username')

        await addchannelcheck(name, username, channelid)
        await message.answer(
            "✅ Kanal ID tayyor bo'ldi.\n\n📢 Kiritgan kanalingiz majburiy obuna qismiga qo'shildi!",
            reply_markup=adminmenu
        )
        await state.finish()
    except ValueError:
        await message.answer("⚠️ Iltimos, faqat raqamdan iborat ID kiriting.")    