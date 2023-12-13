from lexicon.lexicon import lexicon_RU
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton
)


button_go: KeyboardButton = KeyboardButton(text=lexicon_RU['go'])
button_no: KeyboardButton = KeyboardButton(text=lexicon_RU['no'])


keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_go, button_no]],
    resize_keyboard=True,
    one_time_keyboard=True
)