import sqlite3 as sq
import asyncio
from datetime import datetime
import random
import os
import pandas as pd

async def connect_db():
    conn = sq.connect('database.db')
    cur = conn.cursor()
    return conn, cur

async def movie_table():
    conn, cur = await connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Movies 
        (
            MovieID,
            MovieCaption,
            MovieCode
        )        
    """)
    conn.commit()
    conn.close()



async def request_table():
    conn, cur = await connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Requesed 
        (
            userid BIGINT,
            channelid BIGINT
        )        
    """)
    conn.commit()
    conn.close()


async def get_id_channels(user_id: int):
    conn, cur = await connect_db()

    cur.execute("SELECT channelid FROM Requesed WHERE userid = ?", (user_id,))
    channels = cur.fetchall()  
    conn.close()
    channel_ids = [channel[0] for channel in channels]
    return channel_ids
    


async def save_request_to_db(user_id: int, channel_id: int):
    conn, cur = await connect_db()
    
    # Avval foydalanuvchi allaqachon request tashlagan-tashlamaganini tekshiramiz
    cur.execute("SELECT * FROM Requesed WHERE userid = ? AND channelid = ?", (user_id, channel_id))
    existing_request = cur.fetchone()

    if not existing_request:
        # Agar request bazada yo‘q bo‘lsa, qo‘shamiz
        cur.execute("INSERT INTO Requesed (userid, channelid) VALUES (?, ?)", (user_id, channel_id))
        print(f"✅ Foydalanuvchi ({user_id}) ning requesti kanal ({channel_id}) uchun bazaga saqlandi.")
    
    conn.commit()
    conn.close()



async def channels_table():
    conn, cur = await connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Channels 
        (
            ChannelName VARCHAR(255),
            Channelusername VARCHAR(255) NOT NULL,
            Channelid VARCHAR(255) NOT NULL
        )        
    """)
    
    conn.commit()
    conn.close()      


async def users_table():
    conn, cur = await connect_db()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Users 
        (
            name VARCHAR(255),
            username VARCHAR(255),
            userid VARCHAR(255) NOT NULL
        )        
    """)
    
    conn.commit()
    conn.close()  


async def adduser(name, username, userid):
    conn, cur = await connect_db()

    cur.execute("SELECT COUNT(*) FROM Users WHERE userid = ?", (userid,))
    result = cur.fetchone()

    if result[0] == 0:
        cur.execute("""
            INSERT INTO Users (name, username, userid)
            VALUES (?, ?, ?)
        """, (name, username, userid))
        conn.commit()
        conn.close()
    else:
        conn.close()


async def find_channel_usernames():
    conn, cur = await connect_db()
    cur.execute("SELECT ChannelName, Channelusername FROM Channels")
    usernames = cur.fetchall()
    conn.close()

    if usernames:
        return [f"{channel[0]} - {channel[1]}" for channel in usernames]
    return []

async def find_channel_info():
    conn, cur = await connect_db()
    cur.execute("SELECT ChannelName, ChannelUsername, Channelid FROM Channels")
    channel_info = cur.fetchall()
    
    return [(channel[0], channel[1], channel[2]) for channel in channel_info]  # (name, username, id) tuplar ko'rinishida qaytadi



async def find_channel_ids():
    conn, cur = await connect_db()
    cur.execute("SELECT Channelid FROM Channels")
    channel_ids = cur.fetchall()
    
    return [channel_id[0] for channel_id in channel_ids]
async def addchannelcheck(ChannelName, Channelusername, Channelid):
    
    conn, cur = await connect_db()
    cur.execute("""
            INSERT INTO Channels VALUES (?,?,?)""",(ChannelName,Channelusername,Channelid))
    conn.commit()
    conn.close()

async def deletechannelcheck(channelid):
    conn, cur = await connect_db()
    cur.execute("DELETE FROM Channels WHERE Channelid = ?", (channelid,))
    
    conn.commit()
    
    conn.close()

async def generate_unique_movie_code():
    conn, cur = await connect_db()
    
    while True:
        random_code = random.randint(10000, 99999)
        
        cur.execute("SELECT 1 FROM Movies WHERE MovieCode = ?", (random_code,))
        result = cur.fetchone()
        
        if not result: 
            conn.close()
            return random_code    
        
async def addmoviebot(MovieID, MovieCaption, MovieCode):
    conn, cur = await connect_db()
    cur.execute("""
            INSERT INTO Movies (MovieID, MovieCaption, MovieCode)
            VALUES (?, ?, ?)
        """, (MovieID, MovieCaption, MovieCode))
    conn.commit()
    conn.close()

async def deletemoviebot(MovieCode):
    conn, cur = await connect_db()
    cur.execute("""DELETE FROM Movies WHERE MovieCode = ?""", (MovieCode,))
    conn.commit()
    conn.close()

async def useridlist():
    conn, cur = await connect_db()

    cur.execute("SELECT userid FROM Users")
    userids = cur.fetchall()

    userids_list = [userid[0] for userid in userids]

    conn.close()
    return userids_list 

async def save_each_table_to_excel():
    conn, cur = await connect_db()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()

    folder = "exels"
    os.makedirs(folder, exist_ok=True)

    saved_files = []

    for table in tables:
        table_name = table[0]
        cur.execute(f"SELECT * FROM {table_name}")
        columns = [desc[0] for desc in cur.description]
        data = cur.fetchall()
        df = pd.DataFrame(data, columns=columns)

        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_name = os.path.join(folder, f"{current_time}_{table_name}.xlsx")

        with pd.ExcelWriter(file_name) as writer:
            df.to_excel(writer, sheet_name=table_name)

        saved_files.append(file_name)

    conn.close()
    print(f"Saved tables: {', '.join(saved_files)}")
    return saved_files

async def findmovie(MovieCode):
    conn, cur = await connect_db()
    cur.execute("SELECT MovieID, MovieCaption FROM Movies WHERE MovieCode = ?", (MovieCode,))
    movie = cur.fetchone()
    conn.close()
    
    if movie:
        return [movie[0], movie[1]]
    else:
        return None  