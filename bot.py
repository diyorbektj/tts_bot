import logging
from tts import va_speak
import os
import random
from transliterate import translit
from db import insert_user, select_user, insert_voice, select_users, select_voices, select_users_all

from aiogram.utils.exceptions import BotBlocked
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

API_TOKEN = '5813651060:AAEsxPbM7Kjpxd0mscV7V65BSzvg-MKBzzg'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class StepAdmin(StatesGroup):
    panel = State()  # Will be represented in storage as 'Form:name'
    send = State()  # Will be represented in storage as 'Form:age'
    static = State() 

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user = select_user(message.from_user.id)
    if user is None:
    	insert_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    	await bot.send_message(chat_id=333458329, text=f'Bot yangi azosi {message.from_user.first_name}')
    await message.reply("Salom men matnlarni ovozli habarga aylantirib beruvchi botman Marhamat matn kiriting!")
    rand = random.randint(10, 9999999999)
    message_lat = translit("Salom men matnlarni ovozli habarga aylantirib beruvchi botman                          Marhamat matn kiriting!", "ru", reversed=True)
    va_speak(message_lat, rand)
    
    with open(str(rand)+'.ogg', 'rb') as photo:
        await message.reply_voice(photo, caption='@ittsrobot')
    os.remove(str(rand)+".ogg")
    
@dp.message_handler(commands=['bot ishla', 'ishla'])
async def send_welcome(message: types.Message):
    users = await select_users_all()
    for user in users:
    	try:
    	    print(user['user_id'])
    	    await bot.send_message(chat_id=user['user_id'], text=f'Diqqat!!! @ittsrobot kodi 30$ ga sotiladi oladigonlar @Diyorbek_TJ ga,urojat qilsin!')
    	except BotBlocked:
            pass


@dp.message_handler(commands=['users'])
async def send_welcome(message: types.Message):
    result = select_users()
    await bot.send_message(chat_id=333458329, text='Foydalunuvchilar umumiy soni: '+ str(result['count']))
    
@dp.message_handler(commands=['voices24', 'test123'])
async def send_welcome(message: types.Message):
    result = select_voices()
    await bot.send_message(chat_id=333458329, text='Foydalunuvchilar umumiy soni: '+ str(result['count']))

@dp.message_handler(commands=['admin', 'test123'])
async def send_welcome(message: types.Message):
    if message.from_user.id == 333458329:
      
    	await StepAdmin.panel.set()

@dp.message_handler(state=StepAdmin.panel)
async def panel(message: types.Message, state: FSMContext):
	if message.text == "test":
		await state.finish()
		await message.reply("ok")

@dp.message_handler()
async def echo(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    if len(message.text) < 450:
    	user = select_user(message.from_user.id)
    	if user is None:
    		insert_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    	await message.reply("Qabul qildim, kutib turing...")
    	rand = random.randint(10, 9999999999)
    	message_lat = translit(message.text, "ru", reversed=True)
    	va_speak(message_lat, rand)
    
    	with open(str(rand)+'.ogg', 'rb') as photo:
        	await message.reply_voice(photo, caption='@ittsrobot')
    	os.remove(str(rand)+".ogg")
    	insert_voice(message.from_user.id, message.from_user.username, message.text)
    else:
    	await message.reply("Text juda uzun")
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
