from aiogram import types
from aiogram.types import ChatJoinRequest
from loader import dp
from database.base import save_request_to_db
from database.base import connect_db


async def delete_request_from_db(user_id: int, chat_id: int):
    db, cur = await connect_db()
    cur.execute("DELETE FROM join_requests WHERE user_id = ? AND chat_id = ?", (user_id, chat_id))
    db.commit()
    db.close()

@dp.chat_join_request_handler()
async def handle_join_request(request: types.ChatJoinRequest):
    user_id = request.from_user.id
    chat_id = request.chat.id

    await save_request_to_db(user_id, chat_id)

    print(f"🔄 Foydalanuvchi ({user_id}) kanal ({chat_id}) ga request tashladi.")
