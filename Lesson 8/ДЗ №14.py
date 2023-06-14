# Задание

# Создайте бот-справочник с красивым меню (используйте KeyBoardButton и ReplyKeyboardMarkup).

# Разделы можете придумать самостоятельно — самое главное, чтобы через меню, которое возвращает бот,
# можно было переходить между разделами и получать информацию от бота.

# Если у вас нет данных, чтобы добавить в справочную информацию, вы можете использовать тексты-заглушки.
# Достаточно реализовать функционал, а наполнение остаётся на ваше усмотрение.


from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters

button_1 = KeyboardButton("Что умеет этот бот")
button_2 = KeyboardButton("Готовые сценарии")
button_3 = KeyboardButton("Начать пользоваться ботом")
button_4 = KeyboardButton("FAQ")
button_5 = KeyboardButton("Настройки")
button_6 = KeyboardButton("Сделать пожертвование")
button_back = KeyboardButton("Назад")


def start(update, _):
    keyboard = [
        [
            button_1,
            button_2,
        ],
        [button_3],
        [
            button_4,
            button_5,
            button_6,
        ]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text('Выберете, что хотите сделать с ботом:', reply_markup=reply_markup)


def help_command(update, _):
    update.message.reply_text("Используйте `/start` для начала работы с ботом.")


def b_back():
    keyboard2 = [[button_back]]
    reply_markup = ReplyKeyboardMarkup(keyboard2)
    return reply_markup


def b_1(update: Update, context: CallbackContext):
    update.message.reply_text('Этот бот умеет кричать: '
                              'ААААААААААААААААААААААААААААААААААААААА', reply_markup=b_back())


def b_2(update: Update, context: CallbackContext):
    update.message.reply_text('В готовых сценариях бот тоже кричит: '
                              'ААААААААААААААААААААААААААААААААААААААА', reply_markup=b_back())


def b_3(update: Update, context: CallbackContext):
    update.message.reply_text('Окей, бот кричит: '
                              'ААААААААААААААААААААААААААААААААААААААА', reply_markup=b_back())


def b_4(update: Update, context: CallbackContext):
    update.message.reply_text('Всего один популярный вопрос: зачем бот кричит? \n'
                              'Ответ: нет ответа. \n'
                              'ААААААААААААААААААААААААААААААААААААААА', reply_markup=b_back())


def b_5(update: Update, context: CallbackContext):
    update.message.reply_text('Настраивать нечего. '
                              'ААААААААААААААААААААААААААААААААААААААА', reply_markup=b_back())


def b_6(update: Update, context: CallbackContext):
    update.message.reply_text('Да в принципе и без пожертвований можно уже. '
                              'ААААААААААААААААААААААААААААААААААААААА', reply_markup=b_back())


if __name__ == '__main__':

    updater = Updater("ВВЕДИТЕ ТОКЕН БОТА")
    app = updater.dispatcher

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(MessageHandler(Filters.regex("Что умеет этот бот") & ~Filters.command, b_1))
    app.add_handler(MessageHandler(Filters.regex("Готовые сценарии") & ~Filters.command, b_2))
    app.add_handler(MessageHandler(Filters.regex("Начать пользоваться ботом") & ~Filters.command, b_3))
    app.add_handler(MessageHandler(Filters.regex("FAQ") & ~Filters.command, b_4))
    app.add_handler(MessageHandler(Filters.regex("Настройки") & ~Filters.command, b_5))
    app.add_handler(MessageHandler(Filters.regex("Сделать пожертвование") & ~Filters.command, b_6))
    app.add_handler(MessageHandler(Filters.regex("Назад") & ~Filters.command, start))

    updater.start_polling()
    updater.idle()
