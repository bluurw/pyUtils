import asyncio
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram import Dispatcher
from aiogram.utils import executor

import yt_dlp
import os

TOKEN_BOT = ""

bot = Bot(token=TOKEN_BOT)
dp = Dispatcher(bot)

# command HELP START
@dp.message_handler(commands=['help', 'start', 'Help', 'Start'])
async def help_start(message: types.Message):
    await message.reply('''/video: video + https://www.youtube.com/watch?v= 
                            \n/music: music + https://www.youtube.com/watch?v=''')

# command Download Video
@dp.message_handler(commands=['Video', 'video'])
async def video_dowload(message: types.Message):
    params = message.text.split(' ', maxsplit=1)
    for param in params:
        if param == ' ':
            params.remove(param)
    file_path = downloadVideoYt(params[1])
    if file_path[0] == 1:
        await message.reply_document(open(file_path[1], "rb"))
        removeItem(file_path[1])
    else: 
        await message.reply(f'Link: {file_path[1]} not found.')

# command Download Music
@dp.message_handler(commands=['Music', 'music', 'song', 'Song', 'Audio', 'audio'])
async def music_dowload(message: types.Message):
    params = message.text.split(' ', maxsplit=1)
    for param in params:
        if param == ' ':
            params.remove(param)
    file_path = downloadMusicYt(params[1])
    if file_path[0] == 1:
        await message.reply_document(open(file_path[1],"rb"))
        removeItem(file_path[1])
    else: 
        await message.reply(f'Link: {file_path[1]} not found.')



# STRUCTs
def downloadVideoYt(url:str):
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': '%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=True)  # Extract and download
            file_name = ydl.prepare_filename(info_dict) 
            return 1, file_name
    except:
        return 0, url

def downloadMusicYt(url:str):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'outtmpl': '%(title)s.mp3',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=True)  # Extract and download
            file_name = ydl.prepare_filename(info_dict) 
            return 1, file_name
    except:
        return 0, url

def removeItem(file_path:str):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return 1
        else:
            return 0
    except Exception as e:
        return 0

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
































# blurrw =)