# - *- coding: utf- 8 - *-

#Production by Famaxth
#Telegram - @por0vos1k


import db
import typing
import keyboards
import time
import random

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types.chat import ChatActions
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


from os import W_OK
from utils import Work
from config import TOKEN
from messages import MESSAGES
from functions import create_password


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db.init_db()
print("Start")


all_users_file = open("joined.txt", "r")
all_users = set()
for line in all_users_file:
	all_users.add(line.strip())
all_users_file.close()



@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    if str(message.from_user.id) in all_users:

        text = db.return_user_lang(message.from_user.id)
        language = (str(text).replace("('", "")).replace("',)", "")

        if language == "English":
            await bot.send_chat_action(message.from_user.id, action=ChatActions.TYPING)
            await bot.send_message(message.from_user.id, MESSAGES['start_eng'], reply_markup=keyboards.start_eng)

        else:
            await bot.send_chat_action(message.from_user.id, action=ChatActions.TYPING)
            await bot.send_message(message.from_user.id, MESSAGES['start_ru'], reply_markup=keyboards.start_ru)

    else:
        await bot.send_chat_action(message.from_user.id, action=ChatActions.TYPING)
        await bot.send_message(message.from_user.id, "Choose the language.\n\nВыберите язык.", reply_markup=keyboards.lang)



@dp.callback_query_handler(lambda c: c.data == 'Русский')
async def callback_rus(call: types.CallbackQuery):
    if str(call.from_user.id) in all_users:

        db.edit_lang(call.from_user.id, "Russian")
        await bot.send_message(call.from_user.id, "Язык успешно изменен!")
        await bot.send_chat_action(call.from_user.id, action=ChatActions.TYPING)
        await bot.send_message(call.from_user.id, MESSAGES['start_ru'], reply_markup=keyboards.start_ru)

    else:
        all_users_file = open("joined.txt", "a")
        all_users_file.write(str(call.from_user.id) + "\n")
        all_users.add(str(call.from_user.id))
        text = db.add_user(call.from_user.id, "Russian")
        await bot.send_message(call.from_user.id, "Язык успешно изменен!")
        await bot.send_chat_action(call.from_user.id, action=ChatActions.TYPING)
        await bot.send_message(call.from_user.id, MESSAGES['start_ru'], reply_markup=keyboards.start_ru)



@dp.callback_query_handler(lambda c: c.data == 'English')
async def callback_eng(call: types.CallbackQuery):
    if str(call.from_user.id) in all_users:

        db.edit_lang(call.from_user.id, "English")
        await bot.send_message(call.from_user.id, "The language has changed successfully!")
        await bot.send_chat_action(call.from_user.id, action=ChatActions.TYPING)
        await bot.send_message(call.from_user.id, MESSAGES['start_eng'], reply_markup=keyboards.start_eng)

    else:
        all_users_file = open("joined.txt", "a")
        all_users_file.write(str(call.from_user.id) + "\n")
        all_users.add(str(call.from_user.id))
        db.add_user(call.from_user.id, "English")
        await bot.send_message(call.from_user.id, "The language has changed successfully!")
        await bot.send_chat_action(call.from_user.id, action=ChatActions.TYPING)
        await bot.send_message(call.from_user.id, MESSAGES['start_eng'], reply_markup=keyboards.start_eng)



@dp.callback_query_handler(lambda c: c.data == 'Создать пароль', state=None)
async def length_ru(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "<a><b>Внимание! Вся информация, которую вы будете собираетесь вводить ниже, будет использоваться в качестве параметров для создания пароля.</b>\n\nВведите длину пароля:</a>", parse_mode='HTML')
    await Work.Length.set()



@dp.callback_query_handler(lambda c: c.data == 'Create Password', state=None)
async def length_eng(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(call.from_user.id, "<a><b>Attention! All the information you will be going to enter below, it will be used as parameters for creating a password.</b>\n\nEnter the password length:</a>", parse_mode='HTML')
    await Work.Length.set()



@dp.message_handler(state=Work.Length)
async def special_symbol(message: types.Message, state: FSMContext):

    text = db.return_user_lang(message.from_user.id)
    language = (str(text).replace("('", "")).replace("',)", "")

    if language == "English":
        try:
            if int(message.text) >= 1 and int(message.text) <= 100:

                async with state.proxy() as data:
                    data["length"] = int(message.text)

                await bot.send_message(message.from_user.id, """Do you want to use special characters?\n\nExample: %, *, ),?, @, #, $, ~""")
                await Work.Special_symbol.set()
            else:
                await message.reply("❌")
                await bot.send_message(message.from_user.id, "Error! Valid numbers from 1 to 100.")
                await Work.Length.set()
        except:
            await message.reply("❌")
            await bot.send_message(message.from_user.id, "Error! You must enter a number.\n\nExample: 12")
            await Work.Length.set()

    else:
        try:
            if int(message.text) >= 1 and int(message.text) <= 100:

                async with state.proxy() as data:
                    data["length"] = int(message.text)

                await bot.send_message(message.from_user.id, """Хотите использовать спец. символы?\n\nПример: %, *, ),?, @, #, $, ~""")
                await Work.Special_symbol.set()
            else:
                await message.reply("❌")
                await bot.send_message(message.from_user.id, "Ошибка! Допустимые числа от 1 до 100")
                await Work.Length.set()
        except:
            await message.reply("❌")
            await bot.send_message(message.from_user.id, "Ошибка! Необходимо ввести цифру.\n\nПример: 12")
            await Work.Length.set()



@dp.message_handler(state=Work.Special_symbol)
async def big_symbol(message: types.Message, state: FSMContext):

    text = db.return_user_lang(message.from_user.id)
    language = (str(text).replace("('", "")).replace("',)", "")

    if language == "English":
        try:
            if (str(message.text)).lower() == "yes":

                async with state.proxy() as data:
                    data["special_symbol"] = True

                await bot.send_message(message.from_user.id, "Do you want to use large letters A-Z?")
                await Work.Big_symbol.set()
            else:

                async with state.proxy() as data:
                    data["special_symbol"] = False

                await bot.send_message(message.from_user.id, "Do you want to use large letters A-Z?")
                await Work.Big_symbol.set()
        except:
            await message.reply("❌")
            await bot.send_message(message.from_user.id, 'Error! You can only answer with the text "Yes" or " No".')
            await Work.Special_symbol.set()

    else:
        try:
            if (str(message.text)).lower() == "да":

                async with state.proxy() as data:
                    data["special_symbol"] = True

                await bot.send_message(message.from_user.id, "Вы хотите использовать заглавные буквы A-Z?")
                await Work.Big_symbol.set()
            else:

                async with state.proxy() as data:
                    data["special_symbol"] = False

                await bot.send_message(message.from_user.id, "Вы хотите использовать заглавные буквы A-Z?")
                await Work.Big_symbol.set()
        except:
            await message.reply("❌")
            await bot.send_message(message.from_user.id, 'Ошибка! Вы можете ответить только текстом "Да" или "Нет".')
            await Work.Special_symbol.set()



@dp.message_handler(state=Work.Big_symbol)
async def numbers(message: types.Message, state: FSMContext):

    text = db.return_user_lang(message.from_user.id)
    language = (str(text).replace("('", "")).replace("',)", "")

    if language == "English":
        try:
            if (str(message.text)).lower() == "yes":

                async with state.proxy() as data:
                    data["big_symbol"] = True

                await bot.send_message(message.from_user.id, "Do we use numbers 0-9?")
                await Work.Numbers.set()
            else:

                async with state.proxy() as data:
                    data["big_symbol"] = False

                await bot.send_message(message.from_user.id, "Do we use numbers 0-9?")
                await Work.Numbers.set()
        except:
            await message.reply("❌")
            await bot.send_message(message.from_user.id, 'Error! You can only answer with the text "Yes" or " No".')
            await Work.Big_symbol.set()

    else:

        try:
            if (str(message.text)).lower() == "да":

                async with state.proxy() as data:
                    data["big_symbol"] = True

                await bot.send_message(message.from_user.id, "Будем использовать цифры 0-9?")
                await Work.Numbers.set()
            else:

                async with state.proxy() as data:
                    data["big_symbol"] = False

                await bot.send_message(message.from_user.id, "Будем использовать цифры 0-9?")
                await Work.Numbers.set()
        except:
            await message.reply("❌")
            await bot.send_message(message.from_user.id, 'Ошибка! Вы можете ответить только текстом "Да" или "Нет".')
            await Work.Big_symbol.set()



@dp.message_handler(state=Work.Numbers)
async def small_symbol(message: types.Message, state: FSMContext):

    text = db.return_user_lang(message.from_user.id)
    language = (str(text).replace("('", "")).replace("',)", "")

    if language == "English":
        try:
            if (str(message.text)).lower() == "yes":

                async with state.proxy() as data:
                    data["numbers"] = True

                await bot.send_message(message.from_user.id, "Do you want to use lowercase letters a-z?")
                await Work.Small_symbol.set()
            else:

                async with state.proxy() as data:
                    data["numbers"] = False

                await bot.send_message(message.from_user.id, "Do you want to use lowercase letters a-z?")
                await Work.Small_symbol.set()
        except:
            await message.reply("❌")
            await bot.send_message(message.from_user.id, 'Error! You can only answer with the text "Yes" or " No".')
            await Work.Numbers.set()

    else:
        try:
            if (str(message.text)).lower() == "да":

                async with state.proxy() as data:
                    data["numbers"] = True

                await bot.send_message(message.from_user.id, "Вы хотите использовать строчные буквы a-z?")
                await Work.Small_symbol.set()
            else:

                async with state.proxy() as data:
                    data["numbers"] = False

                await bot.send_message(message.from_user.id, "Вы хотите использовать строчные буквы a-z?")
                await Work.Small_symbol.set()
        except:
            await message.reply("❌")
            await bot.send_message(message.from_user.id, 'Ошибка! Вы можете ответить только текстом "Да" или "Нет".')
            await Work.Numbers.set()



@dp.message_handler(state=Work.Small_symbol)
async def stop(message: types.Message, state: FSMContext):

    text = db.return_user_lang(message.from_user.id)
    language = (str(text).replace("('", "")).replace("',)", "")

    if language == "English":
        try:

            if (str(message.text)).lower() == "yes":

                async with state.proxy() as data:
                    data["small_symbol"] = True

                length = data["length"]
                special_symbol = data["special_symbol"]
                big_symbol = data["big_symbol"]
                numbers = data["numbers"]
                small_symbol = data["small_symbol"]
                text = create_password(length, special_symbol, big_symbol, numbers, small_symbol)
                await bot.send_message(message.from_user.id, "<a>Your new password:\n\n<pre>{}</pre></a>".format(text), parse_mode='HTML')
                await state.finish()

            else:

                async with state.proxy() as data:
                    data["small_symbol"] = True

                length = data["length"]
                special_symbol = data["special_symbol"]
                big_symbol = data["big_symbol"]
                numbers = data["numbers"]
                small_symbol = data["small_symbol"]
                try:
                    text = create_password(length, special_symbol, big_symbol, numbers, small_symbol)
                    await bot.send_message(message.from_user.id, "<a>Your new password:\n\n<pre>{}</pre></a>".format(text), parse_mode='HTML')
                except:
                    await bot.send_message(message.from_user.id, "<a>Your new password:\n\n<pre>absent</pre></a>", parse_mode='HTML')
                await state.finish()
        except:
            await message.reply("❌")
            await bot.send_message(message.from_user.id, 'Error! You can only answer with the text "Yes" or " No".')
            await Work.Small_symbol.set()

    else:

        try:

            if (str(message.text)).lower() == "да":

                async with state.proxy() as data:
                    data["small_symbol"] = True

                length = data["length"]
                special_symbol = data["special_symbol"]
                big_symbol = data["big_symbol"]
                numbers = data["numbers"]
                small_symbol = data["small_symbol"]
                text = create_password(length, special_symbol, big_symbol, numbers, small_symbol)
                await bot.send_message(message.from_user.id, "<a>Ваш новый пароль:\n\n<pre>{}</pre></a>".format(text), parse_mode='HTML')
                await state.finish()

            else:

                async with state.proxy() as data:
                    data["small_symbol"] = False

                length = data["length"]
                special_symbol = data["special_symbol"]
                big_symbol = data["big_symbol"]
                numbers = data["numbers"]
                small_symbol = data["small_symbol"]
                try:
                    text = create_password(length, special_symbol, big_symbol, numbers, small_symbol)
                    await bot.send_message(message.from_user.id, "<a>Ваш новый пароль:\n\n<pre>{}</pre></a>".format(text), parse_mode='HTML')
                except:
                    await bot.send_message(message.from_user.id, "<a>Ваш новый пароль:\n\n<pre>отсутствует</pre></a>", parse_mode='HTML')
                await state.finish()
        except:
            await message.reply("❌")
            await bot.send_message(message.from_user.id, 'Ошибка! Вы можете ответить только текстом "Да" или "Нет".')
            await Work.Small_symbol.set()



#Запуск бота
if __name__ == '__main__':
    executor.start_polling(dp)