from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


lang = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='English', callback_data='English'))
lang.add(InlineKeyboardButton(text='Русский', callback_data='Русский'))

start_ru = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Создать пароль', callback_data='Создать пароль'))

start_eng = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Create Password', callback_data='Create Password'))