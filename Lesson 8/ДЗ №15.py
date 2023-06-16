# Задание
#
# Создайте Telegram-бота для анкетирования пользователей.
#
# Вопросы и данные придумайте самостоятельно.
#
# Бот должен содержать минимум 3 вопроса, а данные должны сохраняться в SQLite.

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters
from database import save_user, get_user, save_answer

updater = Updater("ВСТАВЬТЕ ТОКЕН БОТА")
app = updater.dispatcher

button_1 = KeyboardButton("Что умеет этот бот")
button_2 = KeyboardButton("Сделать пожертвование")
button_3 = KeyboardButton("Вопрос 1")
button_4 = KeyboardButton("Вопрос 2")
button_5 = KeyboardButton("Вопрос 3")
button_6 = KeyboardButton("Сделать пожертвование")
button_back = KeyboardButton("Назад")

keyboard = [
    [
        button_1,
        button_2,
    ],
    [
        button_3,
        button_4,
        button_5
    ]
]
keyboard2 = [[button_back]]


def start(update, context):
    tgid = update.effective_user.id
    nickname = update.effective_user.username
    if get_user(tgid):
        pass
    else:
        save_user(tgid, nickname)
    update.message.reply_text("Привет! Ответь, пожалуйста, на вопросы",
                              reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False))


def help_command(update, _):
    update.message.reply_text("Используйте `/start` для начала работы с ботом.")


def b_1(update: Update, context: CallbackContext):
    update.message.reply_text('Этот бот проведет небольшое анкетирование',
                              reply_markup=ReplyKeyboardMarkup(keyboard2))


def b_2(update: Update, context: CallbackContext):
    update.message.reply_text('Пожертвований не нужно! Лучше пройдите опрос',
                              reply_markup=ReplyKeyboardMarkup(keyboard2))


def start_poll(update: Update, context: CallbackContext):
    tgid = update.effective_user.id
    if result := get_poll(tgid):
        pass
    else:
        create_poll(tgid)
        result = get_poll(tgid)
    text = f"Ваша анкета - {result}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                             reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False))


def question_1(update: Update, context: CallbackContext):
    text = f"Как вас зовут?"
    context.user_data.update({"is_asked": True, "question_number": 1})
    context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                             reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False))


def question_2(update: Update, context: CallbackContext):
    text = f"Сколько вам лет?"
    context.user_data.update({"is_asked": True, "question_number": 2})
    context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                             reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False))


def question_3(update: Update, context: CallbackContext):
    text = f"Клубнику любите?"
    context.user_data.update({"is_asked": True, "question_number": 3})
    context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                             reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=False))


def poll_result(update: Update, context: CallbackContext):
    tgid = update.effective_user.id
    user_data = get_user(tgid)
    poll_data = get_poll(tgid)
    text = f"Результаты опроса:\n" \
           f"Ваш ИНН - {poll_data[1]}\n" \
           f"Ваc зовут - {poll_data[2]}\n" \
           f"Ваш возраст - {poll_data[3]} лет\n"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text,
                             reply_markup=ReplyKeyboardMarkup(poll_menu, one_time_keyboard=False))


def text_handler(update: Update, context: CallbackContext):
    tgid = update.effective_user.id
    user_status = context.user_data.get("is_asked")
    if user_status:
        question_number = context.user_data["question_number"]
        answer = update.message.text
        save_answer(tgid, question_number, answer)
        context.user_data["is_asked"] = False
        context.bot.send_message(chat_id=update.effective_chat.id, text="Супер!")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Попробуй ответить еще раз")


app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('help', help_command))

app.add_handler(MessageHandler(Filters.regex("Что умеет этот бот") & ~Filters.command, b_1))
app.add_handler(MessageHandler(Filters.regex("Сделать пожертвование") & ~Filters.command, b_2))
app.add_handler(MessageHandler(Filters.regex("start") & ~Filters.command, start_poll))
app.add_handler(MessageHandler(Filters.regex("Вопрос 1") & ~Filters.command, question_1))
app.add_handler(MessageHandler(Filters.regex("Вопрос 2") & ~Filters.command, question_2))
app.add_handler(MessageHandler(Filters.regex("Вопрос 3") & ~Filters.command, question_3))
app.add_handler(MessageHandler(Filters.regex("Назад") & ~Filters.command, start))
app.add_handler(MessageHandler(Filters.regex("Poll results") & ~Filters.command, poll_result))

app.add_handler(MessageHandler(Filters.text & (~Filters.command), text_handler))

if __name__ == '__main__':
    updater.start_polling()
    updater.idle()