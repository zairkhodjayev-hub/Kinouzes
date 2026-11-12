from loader import bot
from database.base import connect_db  # Requestlarni DB dan olish uchun

async def check_subscription(user_id: int, channel_id: int) -> bool:
    try:
        user = await bot.get_chat_member(channel_id, user_id)
        
        if user.status in ("member", "owner", "creator", "administrator"):
            return True
        conn, cur = await connect_db()
        cur.execute("SELECT * FROM Requesed WHERE userid=? AND channelid=?", (user_id, channel_id))
        request_exists = cur.fetchone()
        conn.close()
        
        if request_exists:
            return True

        return False
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        return False
