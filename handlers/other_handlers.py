from aiogram import Router, F
from aiogram.types import Message
from vars_and_queries.game_vars import users
from lexicon.ru_lexicon_functions import reply_other_answers


router: Router = Router()


@router.message(F.text)
async def process_other_answers(message: Message):

    if users[message.from_user.id]['in_game']:
        await message.answer(reply_other_answers(True))

    else:
        await message.answer(reply_other_answers(False))