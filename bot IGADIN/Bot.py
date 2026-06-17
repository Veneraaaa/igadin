from telebot import types
import telebot
import requests

# Токен Telegram-бота
TOKEN = "TOKEN_HERE"

# Trello
TRELLO_KEY = "KEY_HERE"
TRELLO_TOKEN = "TRELLO_TOKEN_HERE"

PROJECTS_BOARD_ID = "68f71a3958dcce5edf3d06f1"

bot = telebot.TeleBot(TOKEN)

project_cards = {}
tender_cards = {}
search_mode = set()


@bot.message_handler(commands=['start'])
def start(message):

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    btn1 = types.KeyboardButton("📁 Проекты")
    btn2 = types.KeyboardButton("🏆 Тендеры")
    btn3 = types.KeyboardButton("📊 Статистика")
    btn4 = types.KeyboardButton("🔍 Поиск")

    markup.add(btn1, btn2)
    markup.add(btn3, btn4)

    bot.send_message(
        message.chat.id,
        "Выберите доску:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "📁 Проекты")
def projects_menu(message):

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.add(types.KeyboardButton("🖊️ Новый проект"))
    markup.add(types.KeyboardButton("🟢 В работе"))
    markup.add(types.KeyboardButton("📋 На согласовании"))
    markup.add(types.KeyboardButton("📄 Договор, заявка"))
    markup.add(types.KeyboardButton("🔧 Установка, монтаж"))
    markup.add(types.KeyboardButton("✅ Завершено"))
    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Выберите раздел:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "🏆 Тендеры")
def tenders_menu(message):

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True
    )

    markup.add(types.KeyboardButton("🖊️ Новый проект"))
    markup.add(types.KeyboardButton("🟢 Тендер"))
    markup.add(types.KeyboardButton("📋 Ожидание решения"))
    markup.add(types.KeyboardButton("📄 Договор"))
    markup.add(types.KeyboardButton("❌ Проиграно/Отказ"))
    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Выберите раздел:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text == "⬅️ Назад")
def back(message):
    start(message)

# =========================
# ПРОЕКТЫ - Новый проект
# =========================

@bot.message_handler(func=lambda message: message.text == "🖊️ Новый проект")
def agreement_projects(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    lists_url = f"https://api.trello.com/1/boards/{PROJECTS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    list_id = None

    for trello_list in lists:
        if trello_list["name"] == "Новый проект":
            list_id = trello_list["id"]
            break

    if not list_id:
        bot.send_message(message.chat.id, "Список не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        project_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Новые проекты:",
        reply_markup=markup
    )


# =========================
# ПРОЕКТЫ - В РАБОТЕ
# =========================

@bot.message_handler(func=lambda message: message.text == "🟢 В работе")
def work_projects(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    lists_url = f"https://api.trello.com/1/boards/{PROJECTS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    work_list_id = None

    for trello_list in lists:
        if trello_list["name"] == "В работе":
            work_list_id = trello_list["id"]
            break

    if not work_list_id:
        bot.send_message(message.chat.id, "Список 'В работе' не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{work_list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        project_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Выберите проект:",
        reply_markup=markup
    )


@bot.message_handler(func=lambda message: message.text in project_cards)
def show_project(message):

    card_id = project_cards[message.text]

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    url = f"https://api.trello.com/1/cards/{card_id}"

    card = requests.get(url, params=params).json()

    text = f"""
📁 {card['name']}

Описание:

{card['desc']}

🔗 Карточка:
{card['url']}
"""

    bot.send_message(
        message.chat.id,
        text
    )

# =========================
# ПРОЕКТЫ - На согласовании
# =========================


@bot.message_handler(func=lambda message: message.text == "📋 На согласовании")
def agreement_projects(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    lists_url = f"https://api.trello.com/1/boards/{PROJECTS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    list_id = None

    for trello_list in lists:
        if trello_list["name"] == "На согласовании":
            list_id = trello_list["id"]
            break

    if not list_id:
        bot.send_message(message.chat.id, "Список не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        project_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Проекты на согласовании:",
        reply_markup=markup
    )

# =========================
# ПРОЕКТЫ - Договор/заявка
# =========================

@bot.message_handler(func=lambda message: message.text == "📄 Договор, заявка")
def agreement_projects(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    lists_url = f"https://api.trello.com/1/boards/{PROJECTS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    list_id = None

    for trello_list in lists:
        if trello_list["name"] == "Договор/заявка":
            list_id = trello_list["id"]
            break

    if not list_id:
        bot.send_message(message.chat.id, "Список не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        project_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Договор на проект:",
        reply_markup=markup
    )

# =========================
# ПРОЕКТЫ - Установка/монтаж
# =========================

@bot.message_handler(func=lambda message: message.text == "🔧 Установка, монтаж")
def agreement_projects(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    lists_url = f"https://api.trello.com/1/boards/{PROJECTS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    list_id = None

    for trello_list in lists:
        if trello_list["name"] == "Установка/монтаж":
            list_id = trello_list["id"]
            break

    if not list_id:
        bot.send_message(message.chat.id, "Список не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        project_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Установка/монтаж:",
        reply_markup=markup
    )

# =========================
# ПРОЕКТЫ - Завершено
# =========================

@bot.message_handler(func=lambda message: message.text == "✅ Завершено")
def agreement_projects(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    lists_url = f"https://api.trello.com/1/boards/{PROJECTS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    list_id = None

    for trello_list in lists:
        if trello_list["name"] == "Завершено":
            list_id = trello_list["id"]
            break

    if not list_id:
        bot.send_message(message.chat.id, "Список не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        project_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Завершенные проекты:",
        reply_markup=markup
    )

# =========================

# =========================
# ТЕНДЕРЫ - Новый проект
# =========================

@bot.message_handler(func=lambda message: message.text == "🖊️ Новый проект")
def work_tenders(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    TENDERS_BOARD_ID = "6a2a899aa353609a85b48ebb"

    lists_url = f"https://api.trello.com/1/boards/{TENDERS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    tender_list_id = None

    for trello_list in lists:
        if trello_list["name"] == "Новый проект":
            tender_list_id = trello_list["id"]
            break

    if not tender_list_id:
        bot.send_message(message.chat.id, "Список не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{tender_list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        tender_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Выберите проект:",
        reply_markup=markup
    )

# =========================
# ТЕНДЕРЫ - Тендер
# =========================

@bot.message_handler(func=lambda message: message.text == "🟢 Тендер")
def work_tenders(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    TENDERS_BOARD_ID = "6a2a899aa353609a85b48ebb"

    lists_url = f"https://api.trello.com/1/boards/{TENDERS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    tender_list_id = None

    for trello_list in lists:
        if trello_list["name"] == "Тендер":
            tender_list_id = trello_list["id"]
            break

    if not tender_list_id:
        bot.send_message(message.chat.id, "Список не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{tender_list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        tender_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Выберите тендер:",
        reply_markup=markup
    )

# =========================
# ТЕНДЕРЫ - Ожидание решения
# =========================

@bot.message_handler(func=lambda message: message.text == "📋 Ожидание решения")
def work_tenders(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    TENDERS_BOARD_ID = "6a2a899aa353609a85b48ebb"

    lists_url = f"https://api.trello.com/1/boards/{TENDERS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    tender_list_id = None

    for trello_list in lists:
        if trello_list["name"] == "Ожидание решения":
            tender_list_id = trello_list["id"]
            break

    if not tender_list_id:
        bot.send_message(message.chat.id, "Список не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{tender_list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        tender_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Выберите проект:",
        reply_markup=markup
    )

# =========================
# ТЕНДЕРЫ - Договор
# =========================

@bot.message_handler(func=lambda message: message.text == "📄 Договор")
def work_tenders(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    TENDERS_BOARD_ID = "6a2a899aa353609a85b48ebb"

    lists_url = f"https://api.trello.com/1/boards/{TENDERS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    tender_list_id = None

    for trello_list in lists:
        if trello_list["name"] == "Договор":
            tender_list_id = trello_list["id"]
            break

    if not tender_list_id:
        bot.send_message(message.chat.id, "Список не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{tender_list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        tender_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Выберите проект:",
        reply_markup=markup
    )

# =========================
# ТЕНДЕРЫ - Проиграно/Отказ
# =========================

@bot.message_handler(func=lambda message: message.text == "❌ Проиграно/Отказ")
def work_tenders(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    TENDERS_BOARD_ID = "6a2a899aa353609a85b48ebb"

    lists_url = f"https://api.trello.com/1/boards/{TENDERS_BOARD_ID}/lists"
    lists = requests.get(lists_url, params=params).json()

    tender_list_id = None

    for trello_list in lists:
        if trello_list["name"] == "Проиграно/Отказ":
            tender_list_id = trello_list["id"]
            break

    if not tender_list_id:
        bot.send_message(message.chat.id, "Список не найден")
        return

    cards_url = f"https://api.trello.com/1/lists/{tender_list_id}/cards"
    cards = requests.get(cards_url, params=params).json()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for card in cards:
        tender_cards[card["name"]] = card["id"]
        markup.add(types.KeyboardButton(card["name"]))

    markup.add(types.KeyboardButton("⬅️ Назад"))

    bot.send_message(
        message.chat.id,
        "Выберите проект:",
        reply_markup=markup
    )



@bot.message_handler(func=lambda message: message.text in tender_cards)
def show_tender(message):

    card_id = tender_cards[message.text]

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    url = f"https://api.trello.com/1/cards/{card_id}"

    card = requests.get(url, params=params).json()

    text = f"""
🏆 {card['name']}

Описание:

{card['desc']}

🔗 Карточка:
{card['url']}
"""

    bot.send_message(
        message.chat.id,
        text
    )



# =========================
# Статистика
# =========================

@bot.message_handler(func=lambda message: message.text == "📊 Статистика")
def statistics(message):

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    text = "📊 СТАТИСТИКА\n\n"

    # ===== ПРОЕКТЫ =====

    text += "📁 Проекты\n"

    project_lists = requests.get(
        f"https://api.trello.com/1/boards/{PROJECTS_BOARD_ID}/lists",
        params=params
    ).json()

    for trello_list in project_lists:

        cards = requests.get(
            f"https://api.trello.com/1/lists/{trello_list['id']}/cards",
            params=params
        ).json()

        text += f"{trello_list['name']}: {len(cards)}\n"

    text += "\n🏆 Тендеры\n"

    TENDERS_BOARD_ID = "6a2a899aa353609a85b48ebb"

    tender_lists = requests.get(
        f"https://api.trello.com/1/boards/{TENDERS_BOARD_ID}/lists",
        params=params
    ).json()

    for trello_list in tender_lists:

        cards = requests.get(
            f"https://api.trello.com/1/lists/{trello_list['id']}/cards",
            params=params
        ).json()

        text += f"{trello_list['name']}: {len(cards)}\n"

    bot.send_message(
        message.chat.id,
        text
    )


# =========================
# Поиск
# =========================

@bot.message_handler(func=lambda message: message.text == "🔍 Поиск")
def search_button(message):

    search_mode.add(message.chat.id)

    bot.send_message(
        message.chat.id,
        "Введите название проекта или тендера:"
    )

@bot.message_handler(func=lambda message: message.chat.id in search_mode)
def search_text(message):

    search_mode.discard(message.chat.id)

    query = message.text.lower()

    params = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN
    }

    found = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    boards = [
        PROJECTS_BOARD_ID,
        "6a2a899aa353609a85b48ebb"
    ]

    for board_id in boards:

        cards = requests.get(
            f"https://api.trello.com/1/boards/{board_id}/cards",
            params=params
        ).json()

        for card in cards:

            if query in card["name"].lower():

                found = True

                project_cards[card["name"]] = card["id"]
                tender_cards[card["name"]] = card["id"]

                markup.add(
                    types.KeyboardButton(card["name"])
                )

    markup.add(types.KeyboardButton("⬅️ Назад"))

    if found:

        bot.send_message(
            message.chat.id,
            "Найдено:",
            reply_markup=markup
        )

    else:

        bot.send_message(
            message.chat.id,
            "Ничего не найдено"
        )

print("Бот запущен...")
bot.infinity_polling()