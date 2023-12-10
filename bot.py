from config_data import *
from lexicon.lexicon_ru import *
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart, ChatMemberUpdatedFilter, KICKED, MEMBER
from aiogram.types import Message, ChatMemberUpdated
import re, asyncio, aiomysql


async def execute_query(query: str, main_command: str) -> tuple | None:
    async with connection.cursor() as cursor:
        await cursor.execute(query)
        if main_command.lower() == 'select':
            return await cursor.fetchone()


@dp.message(CommandStart())
async def process_start_command(message: Message):

    user_id: int = message.from_user.id
    first_name: int = message.from_user.first_name
    username: str | None = message.from_user.username

    users[user_id]: dict = {
        'in_game': False,
        'secret_number': None,
        'attempts': None
        }
        
    if not await execute_query(select_user_info_query % user_id, 'select'):
        await execute_query(add_user_query % (user_id, username, first_name, 0, 0, 0, 0, 'Active'), 'insert')
        await message.answer(reply_start_command(first_name, False))

    else:
        await message.answer(reply_start_command(first_name, True))


@dp.message(Command(commands=('help')))
async def process_help_command(message: Message):
    await message.answer(reply_help_command())


@dp.message(Command(commands=('statistic')))
async def process_stat_command(message: Message):

    user_id: int = message.from_user.id
    emoticons: tuple[str] = (game_emo, winner_cup_emo, score_emo, win_rate_emo)
    full_name: str = message.from_user.full_name
        
    total_games, wins, total_score, win_rate = await execute_query(select_user_info_query % user_id, 'select')

    await message.answer(reply_statistic_command(full_name, total_games, wins,
                                                 total_score, win_rate, emoticons))
    

@dp.message(Command(commands=('myplace')))
async def process_user_place_command(message: Message):
    user_place: int = int((await execute_query(select_user_place % message.from_user.id, 'select'))[0])
    await message.answer(reply_myplace_command(user_place, user_places_emo))
        

@dp.message(Command(commands=('cancel')))
async def process_cancel_command(message: Message):
        
    user_id: int = message.from_user.id

    if users[user_id]['in_game']:
        users[user_id]['in_game']: bool = False
        await message.answer(reply_cancel_command(True))

    else:
        await message.answer(reply_cancel_command(False))


@dp.message(F.text.isdigit(), lambda x: 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):

    user_id: int = message.from_user.id
    user_secret_number: int = users[user_id]['secret_number']
    user_number: int = int(message.text)

    if users[user_id]['in_game']:

        users[user_id]['attempts'] -= 1

        if user_number == users[user_id]['secret_number']:

            total_games, wins, *_ = await execute_query(select_user_info_query % user_id, 'select')
            win_rate: str = str(int(round(((wins + 1) / (total_games + 1)) * 100)))

            user_attempts: int = users[user_id]['attempts']
            number_attempts: int = ATTEMPTS - user_attempts
            remaining_attempts: int = user_attempts if user_attempts > 0 else 1
            score: int = remaining_attempts * 100
            right_word: str = 'попытку' if number_attempts == 1 else ('попытки', 'попыток')[number_attempts > 4]

            await execute_query(update_user_info_query % (1, score, win_rate + '%', user_id), 'update')
            await message.answer(reply_posit_numbers_answer(number_attempts, right_word, score, user_secret_number))
                
            users[user_id]['in_game']: bool = False

        else:

            await message.answer(reply_neg_numbers_answer(user_number, user_secret_number, False))

            if users[user_id]['attempts'] == 0:

                total_games, wins, *_ = await execute_query(select_user_info_query % user_id, 'select')
                win_rate: str = str(int(round((wins / (total_games + 1)) * 100)))

                await execute_query(update_user_info_query % (0, 0, win_rate + '%', user_id), 'update')

                users[user_id]['in_game']: bool = False

                await message.answer(reply_neg_numbers_answer(user_number, user_secret_number, True))

    else:
        await message.answer(reply_not_in_game_numbers_answer())


@dp.message(F.text, lambda x: re.search(r'в другой раз|по(том|зже)|не|no', x.text.lower()))
async def process_negative_answer(message: Message):

    user_id: int = message.from_user.id
        
    if users[user_id]['in_game']:
        await message.answer(reply_neg_answer(True))

    else:
        await message.answer(reply_neg_answer(False))


@dp.message(Command(commands=('play')))
@dp.message(F.text, lambda x: re.search(r'да|хочу|сыграем|го|можно|yes|go|ok', x.text.lower()))
async def process_positive_answer(message: Message):
        
    user_id: int = message.from_user.id

    if users[user_id]['in_game']:
        await message.answer(reply_play_answer(True))

    else:

        users[user_id]['in_game']: bool = True
        users[user_id]['secret_number']: int = randint(1, 100)
        users[user_id]['attempts']: int = ATTEMPTS

        await message.answer(reply_play_answer(False, ATTEMPTS))


@dp.message(F.text)
async def process_other_answers(message: Message):

    if users[message.from_user.id]['in_game']:
        await message.answer(reply_other_answers(True))

    else:
        await message.answer(reply_other_answers(False))


@dp.my_chat_member(ChatMemberUpdatedFilter(KICKED))
async def process_user_blocked_bot(event: ChatMemberUpdated):
    await execute_query(rename_status_user_query % ('Inactive', event.from_user.id), 'update')


@dp.my_chat_member(ChatMemberUpdatedFilter(MEMBER))
async def process_user_unblocked_bot(event: ChatMemberUpdated):
    await execute_query(rename_status_user_query % ('Active', event.from_user.id), 'update')
    await event.answer(reply_unblocked_bot())


async def main() -> None:
    global connection
    global dp

    config: Config = load_config()
    bot: Bot = Bot(config.tg_bot.bot_token)
    dp: Dispatcher = Dispatcher()

    pool: aiomysql.Pool = await aiomysql.create_pool(
        loop=asyncio.get_running_loop(),
        user=config.db.user,
        password=config.db.password,
        db=config.db.name,
        host=config.db.host,
        port=config.db.port,
        autocommit=True
        )

    async with pool.acquire() as connection:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    
    pool.close()
    await pool.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())