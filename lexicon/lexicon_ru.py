def reply_start_command(first_name: str, old_user: bool) -> str:

    if old_user:
        return f'Здравствуйте {first_name}! Я вас помню, вы уже играли со мной в игру, ' \
            'поэтому правила вам объяснять не нужно. Ну чтож, сыграем в игру как в былые 90-е?'
    
    return f'Здравствуйте {first_name}! Я знаю, что вы новенький и предлагаю вам сыграть со мной в игру "Угадай число". ' \
            'Возможно, вы не знаете правила, так как вы новенький. Поэтому нажмите сюда, чтобы узнать правила /help. ' \
            'А если вы уже знаете правила, то готовы ли вы сыграть со мной в игру?'


def reply_help_command() -> str:
    return '"Угадай число" правила игры: 1) Вы соглашаетесь, либо отказываетесь. Допустим вы согласились, дальнейшие мои действия. ' \
        '2) Я загадываю число от 1 до 100 включительно. 3) Вы отправляете мне в чат число и я говорю угадали ли вы или нет, ' \
        'а также я буду давать вам подсказки к разгадке числа. Ну чтож. Вы готовы сыграть со мной в игру?'


def reply_statistic_command(full_name: str, total_games: int, wins: int,
                            game_score: int, win_rate: str, emoticons: tuple[str]) -> str:
    
    game_emo, winner_cup_emo, score_emo, win_rate_emo = emoticons

    return f"Статистика игрока {full_name}\n\n" \
           f"{game_emo} Всего сыграно игр: {total_games} {game_emo}\n\n" \
           f"{winner_cup_emo} Всего выиграно игр: {wins} {winner_cup_emo}\n\n" \
           f"{score_emo} Всего заработано очков: {game_score} {score_emo}\n\n" \
           f"{win_rate_emo} Процент побед: {win_rate} {win_rate_emo}"


def reply_myplace_command(user_place: int, user_places_emo: str) -> str:
    return f'{user_places_emo} Ваша позиция среди других пользователей: {user_place} {user_places_emo}'


def reply_cancel_command(in_game: bool) -> str:
    
    if in_game:
        return 'Вы вышли из игры. Если захотите сыграть снова - напишите об этом'
    
    return 'А мы и так с вами не играем. Может, сыграем?'


def reply_posit_numbers_answer(number_attempts_guessed: int, right_word: str, score: int, hidden_number: int) -> str:

    return f'Поздравляееем!!!! Вы угадали число за {number_attempts_guessed} {right_word}, вы получаете {score} очков! ' \
           f'Загаданное число было {hidden_number}. Сыграем ещё раз?'
    
    
def reply_neg_numbers_answer(user_number: int, hidden_number: int, zero_attempts: bool) -> str:

    default_negative_answer: str = f"К сожалению, вы не угадали. Загаданное число {('больше', 'меньше')[user_number > hidden_number]}"
    
    if zero_attempts:
        return 'К сожалению, у вас больше не осталось попыток. Вы проиграли. ' \
            f'Загаданное число было {hidden_number}. ' \
            'Попробуйте сыграть ещё раз, может повезёт!'
    
    return default_negative_answer


def reply_not_in_game_numbers_answer() -> str:
    return 'Мы ещё не играем. Куда числа отправляете молодой. Хотите сыграть?'


def reply_neg_answer(in_game: bool) -> str:

    if in_game:
        return 'Мы же сейчас с вами играем, присылайте пожалуйста числа от 1 до 100. ' \
        'Если хотите выйти из игры намжите сюда /cancel'
    
    return 'Жаль, если захотите поиграть - просто напишите об этом'


def reply_play_answer(in_game: bool, attempts: int = None) -> str:

    if in_game:
        return 'Пока мы играем в игру я могу реагировать только на числа от 1 до 100 и команды /cancel и /statistic'
    
    return f'Ура! Я загадал число от 1 до 100, попробуй отгадать! У тебя всего {attempts} попыток'


def reply_other_answers(in_game: bool) -> str:

    if in_game:
        return 'Мы же с вами уже играем. Отправляйте, пожалуйста, числа от 1 до 100'
    
    return 'Моя твоя не понимать! Давай просто сыграем в игру!!!'


def reply_unblocked_bot() -> str:
    return 'Я рад видеть тебя снова!'