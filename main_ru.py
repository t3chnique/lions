# ----------------------------------------------- #
# Project Name          : lions       			  #
# Author Name           : Lev Babushkin           #
# File Name             : main.py                 #
# Contact in telegram   : @levaau                 #
# ----------------------------------------------- #
import telebot
import random
import sqlite3
import signal
import sys
import time
import os
from telebot import types
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')
me = os.getenv('ME')

bot = telebot.TeleBot(token)
# ----------------------------------------------- #


def exit_gracefully(signal, frame):
    print(" Stopping the bot...")
    print("# ---------------------end((------------------------- #\n")
    bot.send_message(me, "shutting down...")
    sys.exit(0)


signal.signal(signal.SIGINT, exit_gracefully)

get_data = "SELECT quser_name, soulmate_name, user_task, " \
           "user_2task, user_3task, task_cost, task_2cost, " \
           "task_3cost, user_reward, reward_cost, user_2reward, " \
           "reward_2cost, user_3reward, reward_3cost, l_balance " \
           "FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)"


while True:
    try:
        # ----------------------------------------------- #
        # MADE:

        # fix terminal, make a protection of user_id

        # NEED: delete useless messages, add custom font, allow 2
        # users to work on the same database. make a real donation request,
        # design repeater, make suggest button in registration and editting
        # X-step tutorial with buttons
        print("\n# ---------------------start-------------------------- #")
        print("hello, this is a small addition to the bot")
        bot.send_message(me, "turning on...")

        @bot.message_handler(commands=["search"])
        def search(message):
            bot.send_message(
                message.chat.id, "Please enter the name "
                "of the SQL database file.")
            bot.register_next_step_handler(message, search_database)

        def search_database(message):
            try:
                db_filename = message.text.strip().lower() + '.db'
                conn = sqlite3.connect(db_filename)
                cursor = conn.cursor()
                cursor.execute(get_data)

                user_data = cursor.fetchone()
                conn.close()
                if user_data:
                    (
                        quser_name,
                        soulmate_name,
                        user_task,
                        user_2task,
                        user_3task,
                        task_cost,
                        task_2cost,
                        task_3cost,
                        user_reward,
                        reward_cost,
                        user_2reward,
                        reward_2cost,
                        user_3reward,
                        reward_3cost,
                        l_balance,
                    ) = user_data

                    response = (
                        f"💖{quser_name} и {soulmate_name}💖\n"
                        f"Ваши задания:\n"
                        f"1. {user_task} - за {task_cost} львят\n"
                        f"2. {user_2task} - за {task_2cost} львят\n"
                        f"3. {user_3task} - за {task_3cost} львят\n"
                        f"Ваши награды:\n"
                        f"1. {user_reward} - за {reward_cost} львят\n"
                        f"2. {user_2reward} - за {reward_2cost} львят\n"
                        f"3. {user_3reward} - за {reward_3cost} львят\n"
                        f"Баланс львят: {l_balance}")
                bot.send_message(me, response)
            except Exception as e:
                bot.send_message(
                    message.chat.id,
                    f"An error occurred "
                    f"while searching the database: {str(e)}",
                )

        def get_user_db(user_id):
            conn = sqlite3.connect(f"{user_id}.db")
            cursor = conn.cursor()
            return conn, cursor

        def create_user_table(user_id):
            conn, cursor = get_user_db(user_id)
            cursor.execute("""CREATE TABLE IF NOT EXISTS userdata
                            (id INTEGER PRIMARY KEY AUTOINCREMENT,
                            quser_name TEXT, soulmate_name TEXT,
                            user_task TEXT, user_2task TEXT,
                            user_3task TEXT, task_cost INTEGER,
                            task_2cost INTEGER, task_3cost INTEGER,
                            user_reward TEXT, user_2reward TEXT,
                            user_3reward TEXT, reward_cost INTEGER,
                            reward_2cost INTEGER, reward_3cost INTEGER,
                            l_balance INTEGER DEFAULT 0)""")
            conn.commit()
            conn.close()

        @bot.message_handler(commands=["start"])
        def greet_user(message):
            try:
                user_id = message.from_user.id
                conn, cursor = get_user_db(user_id)
                cursor.execute(
                    "SELECT quser_name, soulmate_name, "
                    "user_task, user_2task, user_3task, "
                    "task_cost, task_2cost, task_3cost, "
                    "user_reward, reward_cost, user_2reward, "
                    "reward_2cost, user_3reward, reward_3cost, "
                    "l_balance FROM userdata WHERE id = "
                    "(SELECT MAX(id) FROM userdata)"
                )
                user_data = cursor.fetchone()
                conn.close()
                if user_data:
                    (
                        quser_name,
                        soulmate_name,
                        user_task,
                        user_2task,
                        user_3task,
                        task_cost,
                        task_2cost,
                        task_3cost,
                        user_reward,
                        reward_cost,
                        user_2reward,
                        reward_2cost,
                        user_3reward,
                        reward_3cost,
                        l_balance,
                    ) = user_data

                    response = (
                        f"💖{quser_name} и {soulmate_name}💖\n"
                        f"Ваши задания:\n"
                        f"1. {user_task} - за {task_cost} львят\n"
                        f"2. {user_2task} - за {task_2cost} львят\n"
                        f"3. {user_3task} - за {task_3cost} львят\n"
                        f"Ваши награды:\n"
                        f"1. {user_reward} - за {reward_cost} львят\n"
                        f"2. {user_2reward} - за {reward_2cost} львят\n"
                        f"3. {user_3reward} - за {reward_3cost} львят\n"
                        f"Баланс львят: {l_balance}")

                photo = "lions2.jpeg"
                file = open("./" + photo, "rb")
                bot.send_photo(user_id, file)
                bot.send_message(user_id, response)
                markup = telebot.types.InlineKeyboardMarkup()
                button1 = telebot.types.InlineKeyboardButton(
                    "да", callback_data="button1")
                button2 = telebot.types.InlineKeyboardButton(
                    "нет", callback_data="button2")
                markup.add(button1, button2)
                bot.send_message(user_id, "Хотите внести изменения?",
                                 reply_markup=markup)
            except Exception:
                user_id = message.from_user.id
                create_user_table(user_id)
                markup = telebot.types.InlineKeyboardMarkup()
                button1 = telebot.types.InlineKeyboardButton(
                    "дальше", callback_data="tut1")
                markup.add(button1)
                photo = "lions_share.jpeg"
                file = open("./" + photo, "rb")
                response = ('Отношения - это искусство создания '
                            'красивых воспоминаний. C помощью этого бота '
                            'вы сможете превратить обыденные задачи в '
                            'чудесные приключения. Создавайте задания '
                            'для вашего партнера, назначайте им цену в '
                            'львятах и наблюдайте, как начинается '
                            'веселье.\nПредставьте, что вы зарабатываете '
                            'львят за выполнение задач, таких как "Помыть '
                            'посуду" или "Сходить за продуктами". Чем '
                            'больше львят вы зарабатываете, тем больше '
                            'наград вас ожидает.')
                bot.send_photo(user_id, file, caption=response,
                               reply_markup=markup)

        def tutorial2(message):
            user_id = message.from_user.id
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "дальше", callback_data="tut2")
            markup.add(button1)
            photo = "lions_share.jpeg"
            file = open("./" + photo, "rb")
            response = ('Для поддержания романтики в отношениях удивляйте '
                        'своего партнера значимыми наградами. "Поход в '
                        'ресторан" или "Завтрак в постели" — всего лишь '
                        'несколько идей. C этим ботом вы можете обмениваться '
                        'львятами и наслаждаться этими наградами вдвоем, '
                        'делая каждый день особенным.')

            bot.send_photo(user_id, file, caption=response,
                           reply_markup=markup)

        def tutorial3(message):
            user_id = message.from_user.id
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "дальше", callback_data="tut3")
            markup.add(button1)
            photo = "lions_share.jpeg"
            file = open("./" + photo, "rb")
            response = ('Регистрация и '
                        'меню:\nПосле завершения туториала '
                        'приложение попросит вас указать ваше имя и '
                        'другую информацию. Вы придумаете задачи, '
                        'награды и их цены в львятах для вашего '
                        'партнера.\n\nНазначение львят:\n'
                        'После регистрации вы увидете меню, '
                        'оно с картинкой львенка. В нем вы можете '
                        'прибавлять и вычитать львят с вашего баланса.')

            bot.send_photo(user_id, file, caption=response,
                           reply_markup=markup)

        def tutorial4(message):
            user_id = message.from_user.id
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "дальше", callback_data="tut4")
            markup.add(button1)
            photo = "lions_share.jpeg"
            file = open("./" + photo, "rb")
            response = ('В левом нижнем углу приложения вы найдете удобное '
                        'меню, '
                        'которое обеспечивает быстрый доступ к основным '
                        'функциям:\n\nProfile: Просмотр вашего профиля, '
                        'который включает в себя список ваших задач, '
                        'наград, их стоимость и баланс львят.\n\n'
                        'Suggest: Получите вдохновение, генерируя 3 случайных '
                        'задачи и 3 случайных награды, когда вам нужны свежие '
                        'идеи.\n\nMain: Это доступ к меню, '
                        'где вы легко можете управлять балансом львят. '
                        'Добавьте '
                        'или уберите львят всего несколькими касаниями.\n\n'
                        'Help: Возникли трудности? Эта кнопка отправит '
                        'туториал заново, а если это не решит проблему - '
                        'по отправленной ссылке вы сможете написать нам.\n\n'
                        'Share: Поделитесь уникальным кодом с вашим '
                        'партнером, позволяя ему или ей присоединиться к '
                        'использованию этого бота. Это отличный способ '
                        'вместе наслаждаться приложением.\n\nConnect: '
                        'Выберете это чтобы ввести код вашего партнера, '
                        'Это откроет возможность просматривать '
                        'и редактировать приложение '
                        'вместе, дополнительно укрепляя вашу связь.')
            bot.send_photo(user_id, file, caption=response,
                           reply_markup=markup)

        def ask_quser_name(message):
            user_id = message.from_user.id
            quser_name = message.text.strip().lower()
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "INSERT INTO userdata (quser_name, l_balance) VALUES (?, 0)",
                (quser_name, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Отлично! Теперь мне бы хотелось узнать "
                             "имя вашей второй половинки")

            bot.register_next_step_handler(message, ask_soulmate_name)

        # Function to record the user's soulmate_name in the database
        def ask_soulmate_name(message):
            user_id = message.from_user.id
            soulmate_name = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET soulmate_name = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (soulmate_name, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Спасибо! Какую первую задачу "
                             "вы хотели бы создать для вашей второй "
                             "половинки?")

            bot.register_next_step_handler(message, ask_user_task)

        # ----------------------------------------------- #

        def ask_user_task(message):
            user_id = message.from_user.id
            user_task = message.text.strip().lower()
            # sql
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_task = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (user_task, ),
            )
            conn.commit()
            conn.close()
            # cost
            bot.send_message(user_id, "Замечательно! Сколько "
                             "львят ваша вторая половинка должна "
                             "заработать за выполнение первой задачи?")

            bot.register_next_step_handler(message, ask_task_cost)

        def ask_task_cost(message):
            # cost
            user_id = message.from_user.id
            task_cost = message.text.strip().lower()
            # sql
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  task_cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (task_cost, ),
            )
            conn.commit()
            conn.close()
            # buttons
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "нет", callback_data="button10")
            button2 = telebot.types.InlineKeyboardButton(
                "да", callback_data="button11")
            markup.add(button1, button2)
            bot.send_message(user_id, "Вы хотели бы добавить "
                             "вторую задачу для вашей второй "
                             "половинки?", reply_markup=markup)

        def ask_user_2task(message):
            user_id = message.from_user.id
            user_2task = message.text.strip().lower()
            # sql
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_2task = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (user_2task, ),
            )
            conn.commit()
            conn.close()
            # cost
            bot.send_message(user_id, "Прекрасный выбор! Сколько "
                             "львят должна заработать ваша вторая "
                             "половинка за выполнение второй задачи?")

            bot.register_next_step_handler(message, ask_2task_cost)

        def ask_2task_cost(message):
            user_id = message.from_user.id
            task_2cost = message.text.strip().lower()
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  task_2cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (task_2cost, ),
            )
            conn.commit()
            conn.close()
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "нет", callback_data="button10")
            button2 = telebot.types.InlineKeyboardButton(
                "да", callback_data="button12")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, "Хотели бы вы "
                             "добавить третью задачу для вашей "
                             "второй половинки?", reply_markup=markup)

        def ask_user_3task(message):
            user_id = message.from_user.id
            user_3task = message.text.strip().lower()
            # sql
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_3task = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (user_3task, ),
            )
            conn.commit()
            conn.close()
            # cost
            bot.send_message(user_id, "Отлично! Сколько львят "
                             "должна заработать ваша вторая "
                             "половинка за выполнение третьей задачи?")

            bot.register_next_step_handler(message, ask_3task_cost)

        def ask_3task_cost(message):
            user_id = message.from_user.id
            task_3cost = message.text.strip().lower()
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  task_3cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (task_3cost, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Теперь поговорим о "
                             "наградах. Какую первую награду вы "
                             "хотели бы предложить в обмен на львят?")

            bot.register_next_step_handler(message, ask_reward)

        # ----------------------------------------------- #

        def ask_reward(message):
            user_id = message.from_user.id
            user_reward = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_reward = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (user_reward, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Замечательно! Сколько львят "
                             "должна потратить ваша вторая половинка, "
                             "чтобы получить первую награду?")

            bot.register_next_step_handler(message, ask_reward_cost)

        def ask_reward_cost(message):
            user_id = message.from_user.id
            reward_cost = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  reward_cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (reward_cost, ),
            )
            conn.commit()
            conn.close()

            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "нет", callback_data="button15")
            button2 = telebot.types.InlineKeyboardButton(
                "да", callback_data="button14")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, "Хотели бы вы "
                             "добавить вторую награду для "
                             "вашей второй половинки?", reply_markup=markup)

        def ask_2reward(message):
            user_id = message.from_user.id
            user_2reward = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_2reward = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (user_2reward, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Отлично! Сколько львят "
                             "должна потратить ваша вторая "
                             "половинка, чтобы получить вторую награду?")

            bot.register_next_step_handler(message, ask_2reward_cost)

        def ask_2reward_cost(message):
            user_id = message.from_user.id
            reward_2cost = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  reward_2cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (reward_2cost, ),
            )
            conn.commit()
            conn.close()

            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "нет", callback_data="button15")
            button2 = telebot.types.InlineKeyboardButton(
                "да", callback_data="button17")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, "Хотели бы вы "
                             "добавить третью награду для "
                             "вашей второй половинки?", reply_markup=markup)

        def ask_3reward(message):
            user_id = message.from_user.id
            user_3reward = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_3reward = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (user_3reward, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Отлично! Сколько львят "
                             "должна потратить ваша вторая "
                             "половинка, чтобы получить третью награду?")

            bot.register_next_step_handler(message, ask_3reward_cost)

        def ask_3reward_cost(message):
            user_id = message.from_user.id
            reward_3cost = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  reward_3cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (reward_3cost, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Спасибо за предоставленную "
                             "информацию! Вот что я знаю о вас:")

            send_user_data(message)

        def send_user_data(call):
            user_id = call.from_user.id
            conn, cursor = get_user_db(user_id)
            cursor.execute(get_data)
            user_data = cursor.fetchone()
            conn.close()
            if user_data:
                (
                    quser_name,
                    soulmate_name,
                    user_task,
                    user_2task,
                    user_3task,
                    task_cost,
                    task_2cost,
                    task_3cost,
                    user_reward,
                    reward_cost,
                    user_2reward,
                    reward_2cost,
                    user_3reward,
                    reward_3cost,
                    l_balance,
                ) = user_data

                response = (
                        f"💖{quser_name} и {soulmate_name}💖\n"
                        f"Ваши задания:\n"
                        f"1. {user_task} - за {task_cost} львят\n"
                        f"2. {user_2task} - за {task_2cost} львят\n"
                        f"3. {user_3task} - за {task_3cost} львят\n"
                        f"Ваши награды:\n"
                        f"1. {user_reward} - за {reward_cost} львят\n"
                        f"2. {user_2reward} - за {reward_2cost} львят\n"
                        f"3. {user_3reward} - за {reward_3cost} львят\n"
                        f"Баланс львят: {l_balance}")
            bot.send_message(user_id, response)
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "да", callback_data="button1")
            button2 = telebot.types.InlineKeyboardButton(
                "нет", callback_data="button2")
            markup.add(button1, button2)
            bot.send_message(user_id, "Хотите внести изменения?",
                             reply_markup=markup)

        @bot.message_handler(commands=["main"])
        def call2handler(call):
            user_id = call.from_user.id
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "SELECT quser_name, l_balance FROM userdata "
                "WHERE id = (SELECT MAX(id) FROM userdata)"
            )
            user_data = cursor.fetchone()
            quser_name, l_balance = user_data
            markup = telebot.types.InlineKeyboardMarkup()
            button3 = telebot.types.InlineKeyboardButton(
                "прибавить 🦁", callback_data="button3")
            button4 = telebot.types.InlineKeyboardButton(
                "вычесть 🦁", callback_data="button4")
            markup.row(button3, button4)
            button5 = telebot.types.InlineKeyboardButton(
                "изменить правила", callback_data="button1")
            button6 = telebot.types.InlineKeyboardButton(
                "другое", callback_data="button6")
            markup.row(button5, button6)
            photo = "lions.png"
            file = open("./" + photo, "rb")
            try:
                bot.send_message(call.message.chat.id,
                                 f"Привет, {quser_name}!\n🦁: {l_balance}")
                bot.send_photo(call.message.chat.id, file, reply_markup=markup)
            except Exception:
                bot.send_message(call.chat.id,
                                 f"Привет, {quser_name}!\n🦁: {l_balance}")
                bot.send_photo(call.chat.id, file, reply_markup=markup)

        # ----------------------------------------------- #
        #                   callback                      #
        #                                                 #
        #                                                 #
        #                                                 #
        # ----------------------------------------------- #

        @bot.callback_query_handler(func=lambda call: True)  # main message
        def callback_handler(call):
            user_id = call.from_user.id
            if call.data == "button2":
                call2handler(call)
            elif call.data == "button1":
                bot.send_message(user_id, "Для начала, "
                                 "пожалуйста, скажите мне ваше имя")
                bot.register_next_step_handler(call.message, edit_quser_name)
            elif call.data == "button3":
                bot.send_message(call.message.chat.id, "Сколько?")  # plus
                bot.register_next_step_handler(call.message, pluslions)
            elif call.data == "button4":
                bot.send_message(call.message.chat.id, "Сколько?")  # minus
                bot.register_next_step_handler(call.message, minuslions)
            elif call.data == "button6":
                markup = types.InlineKeyboardMarkup()
                return_button = types.InlineKeyboardButton(
                    "Return", callback_data="button7")
                markup.add(return_button)
                bot.send_message(call.message.chat.id, "you can:")
                bot.send_message(
                    call.message.chat.id,
                    "✨[say thank you](https://www.buymeacoffee.com/)✨",
                    parse_mode="Markdown",
                )
                bot.send_message(
                    call.message.chat.id,
                    "✨[contact me](https://t.me/levaau)✨",
                    parse_mode="Markdown",
                    reply_markup=markup,
                )
            elif call.data == "button7":
                call2handler(call)
            elif call.data == "button8":
                call2handler(call)
            elif call.data == "button9":
                markup = types.InlineKeyboardMarkup()
                return_button = types.InlineKeyboardButton(
                    "Return", callback_data="button7")
                markup.add(return_button)
                bot.send_message(
                    call.message.chat.id,
                    "✨[feel free to contact me](https://t.me/levaau)✨",
                    parse_mode="Markdown",
                    reply_markup=markup,
                )
            elif call.data == "button10":  # same with 13
                bot.send_message(user_id, "Теперь давайте поговорим о "
                                 "наградах. Какую первую награду вы "
                                 "хотели бы предложить в обмен на львят?")

                bot.register_next_step_handler(call.message, ask_reward)
            elif call.data == "button11":
                bot.send_message(
                    user_id,
                    "Фантастика! Какую вторую задачу вы бы хотели "
                    "создать для вашей второй половинки?")
                bot.register_next_step_handler(call.message, ask_user_2task)
            elif call.data == "button12":
                bot.send_message(user_id, "Понял! Какую третью задачу "
                                 "вы хотели бы создать для вашей второй "
                                 "половинки?")

                bot.register_next_step_handler(call.message, ask_user_3task)
            elif call.data == "button14":
                bot.send_message(user_id, "Прекрасный выбор! Какую вторую "
                                 "награду вы хотели бы предложить в обмен "
                                 "на львят?")

                bot.register_next_step_handler(call.message, ask_2reward)
            elif call.data == "button15":
                bot.send_message(user_id, "Спасибо за предоставленную "
                                 "информацию! Вот что я знаю о вас:")
                send_user_data(call)
            elif call.data == "button17":
                bot.send_message(user_id, "Последнее, но не менее важное. "
                                 "Какую третью награду вы хотели бы "
                                 "предложить в обмен на львят?")
                bot.register_next_step_handler(call.message, ask_3reward)
            elif call.data == "button18":
                bot.send_message(user_id, "Теперь поговорим о наградах. "
                                 "Какую первую награду вы хотели бы "
                                 "предложить в обмен на львов?")

                bot.register_next_step_handler(call.message, edit_reward)
            elif call.data == "button19":
                bot.send_message(user_id, "Фантастика! Какую вторую "
                                 "задачу вы бы хотели создать для вашей "
                                 "половинки?")
                bot.register_next_step_handler(call.message, edit_user_2task)
            elif call.data == "button20":
                bot.send_message(user_id, "Понял! Какую третью задачу вы "
                                 "хотели бы создать для вашей второй "
                                 "половинки?")
                bot.register_next_step_handler(call.message, edit_user_3task)
            elif call.data == "button13":
                bot.send_message(user_id, "Прекрасный выбор! Какую вторую "
                                 "награду вы хотели бы предложить в "
                                 "обмен на львят?")
                bot.register_next_step_handler(call.message, ask_2reward)
            elif call.data == "button16":
                bot.send_message(user_id, "Последнее, но не менее важное. "
                                 "Какую третью награду вы хотели бы "
                                 "предложить в обмен на львят?")
                bot.register_next_step_handler(call.message, edit_3reward)
            elif call.data == "tut1":
                tutorial2(call)
            elif call.data == "tut2":
                tutorial3(call)
            elif call.data == "tut3":
                tutorial4(call)
            elif call.data == "tut4":
                bot.send_message(user_id, "Для начала, "
                                 "пожалуйста, скажите мне ваше имя")
                bot.register_next_step_handler(call.message, ask_quser_name)

        def minuslions(message):
            user_id = message.from_user.id
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "SELECT l_balance FROM userdata WHERE id = (SELECT MAX(id) "
                "FROM userdata)"
            )
            user_data = cursor.fetchone()
            if user_data:
                (l_balance, ) = user_data  # Unpack the value from the tuple
                l_balance_new = int(message.text.strip())
                l_balance -= l_balance_new
                cursor.execute(
                    "UPDATE userdata SET  l_balance = ? WHERE id = "
                    "(SELECT MAX(id) FROM userdata)",
                    (l_balance, ),
                )
                conn.commit()
                conn.close()  # end!!!!
                call2handler(message)
            else:
                bot.send_message(
                    user_id,
                    "Error: User data not found. "
                    "Please make sure you have provided your information.",
                )

        def pluslions(message):
            user_id = message.from_user.id
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "SELECT l_balance FROM userdata WHERE id = "
                "(SELECT MAX(id) FROM userdata)"
            )
            user_data = cursor.fetchone()
            if user_data:
                (l_balance, ) = user_data  # Unpack the value from the tuple
                l_balance_new = int(message.text.strip())
                l_balance += l_balance_new
                cursor.execute(
                    "UPDATE userdata SET  l_balance = ? WHERE id = "
                    "(SELECT MAX(id) FROM userdata)",
                    (l_balance, ),
                )
                conn.commit()
                conn.close()  # end!!!!
                call2handler(message)
            else:
                bot.send_message(
                    user_id,
                    "Error: User data not found. "
                    "Please make sure you have provided your information.",
                )

        # ----------------------------------------------- #
        #                   editinfo                      #
        #                                                 #
        #                                                 #
        #                                                 #
        # ----------------------------------------------- #

        @bot.message_handler(commands=["start_edit_info"])
        def start_edit_info(message):
            user_id = message.from_user.id
            bot.send_message(user_id, "Для начала, пожалуйста, "
                             "скажите мне ваше имя")

            bot.register_next_step_handler(message, edit_quser_name)

        def edit_quser_name(message):
            user_id = message.from_user.id
            quser_name = message.text.strip().lower()
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  quser_name = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (quser_name, ),
            )
            conn.commit()
            conn.close()
            bot.send_message(user_id, "Отлично! Теперь мне бы "
                             "хотелось узнать имя вашей второй половинки")
            bot.register_next_step_handler(message, edit_soulmate_name)

        def edit_soulmate_name(message):
            user_id = message.from_user.id
            soulmate_name = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET soulmate_name = ?"
                "WHERE id = (SELECT MAX(id) FROM userdata)",
                (soulmate_name, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Спасибо! Какую первую задачу вы "
                             "хотели бы создать для вашей второй половинки?")
            bot.register_next_step_handler(message, edit_user_task)

        def edit_user_task(message):
            user_id = message.from_user.id
            user_task = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_task = ? WHERE id "
                "= (SELECT MAX(id) FROM userdata)",
                (user_task, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Замечательно! Сколько львят ваша "
                             "вторая половинка должна заработать за "
                             "выполнение первой задачи?")

            bot.register_next_step_handler(message, edit_task_cost)

        def edit_task_cost(message):
            # cost
            user_id = message.from_user.id
            task_cost = message.text.strip().lower()
            # sql
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  task_cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (task_cost, ),
            )
            conn.commit()
            conn.close()
            # buttons
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "нет", callback_data="button18")
            button2 = telebot.types.InlineKeyboardButton(
                "да", callback_data="button19")
            markup.add(button1, button2)
            bot.send_message(user_id, "Вы хотели бы добавить вторую "
                             "задачу для вашей половинки?",
                             reply_markup=markup)

            # bot.register_next_step_handler(message, edit_reward)

        def edit_user_2task(message):
            user_id = message.from_user.id
            user_2task = message.text.strip().lower()
            # sql
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_2task = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (user_2task, ),
            )
            conn.commit()
            conn.close()
            # cost
            bot.send_message(user_id, "Прекрасный выбор! Сколько "
                             "львят должна заработать ваша "
                             "половинка за выполнение второй задачи?")

            bot.register_next_step_handler(message, edit_2task_cost)

        def edit_2task_cost(message):
            user_id = message.from_user.id
            task_2cost = message.text.strip().lower()
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  task_2cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (task_2cost, ),
            )
            conn.commit()
            conn.close()
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "нет", callback_data="button18")
            button2 = telebot.types.InlineKeyboardButton(
                "да", callback_data="button20")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, "Хотели бы вы добавить "
                             "третью задачу для вашей второй половинки?",
                             reply_markup=markup)

        def edit_user_3task(message):
            user_id = message.from_user.id
            user_3task = message.text.strip().lower()
            # sql
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_3task = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (user_3task, ),
            )
            conn.commit()
            conn.close()
            # cost
            bot.send_message(user_id, "Отлично! Сколько львят должна "
                             "заработать ваша вторая половинка за "
                             "выполнение третьей задачи?")

            bot.register_next_step_handler(message, edit_3task_cost)

        def edit_3task_cost(message):
            user_id = message.from_user.id
            task_3cost = message.text.strip().lower()
            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  task_3cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (task_3cost, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Теперь поговорим о наградах. Какую "
                             "первую награду вы хотели бы предложить в "
                             "обмен на львят?")

            bot.register_next_step_handler(message, edit_reward)

        def edit_reward(message):
            user_id = message.from_user.id
            user_reward = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_reward = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (user_reward, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Замечательно! Сколько львят "
                             "должна потратить ваша вторая половинка, "
                             "чтобы получить первую награду?")

            bot.register_next_step_handler(message, edit_reward_cost)

        def edit_reward_cost(message):
            user_id = message.from_user.id
            reward_cost = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  reward_cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (reward_cost, ),
            )
            conn.commit()
            conn.close()

            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "no", callback_data="button15")
            button2 = telebot.types.InlineKeyboardButton(
                "yes", callback_data="button13")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, "Хотели бы вы добавить "
                             "вторую награду для вашей половинки?",
                             reply_markup=markup)

        def edit_2reward(message):
            user_id = message.from_user.id
            user_2reward = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_2reward = ? WHERE "
                "id = (SELECT MAX(id) FROM userdata)",
                (user_2reward, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Отлично! Сколько львят "
                             "должна потратить ваша половинка, чтобы "
                             "получить вторую награду?")

            bot.register_next_step_handler(message, edit_2reward_cost)

        def edit_2reward_cost(message):
            user_id = message.from_user.id
            reward_2cost = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  reward_2cost = ? WHERE id "
                "= (SELECT MAX(id) FROM userdata)",
                (reward_2cost, ),
            )
            conn.commit()
            conn.close()

            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "нет", callback_data="button15")
            button2 = telebot.types.InlineKeyboardButton(
                "да", callback_data="button16")
            markup.add(button1, button2)
            bot.send_message(message.chat.id, "Хотели бы вы добавить "
                             "третью награду для вашей второй половинки?",
                             reply_markup=markup)

        def edit_3reward(message):
            user_id = message.from_user.id
            user_3reward = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  user_3reward = ? WHERE "
                "id = (SELECT MAX(id) FROM userdata)",
                (user_3reward, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Отлично! Сколько львят "
                             "должна потратить ваша вторая половинка, "
                             "чтобы получить третью награду?")

            bot.register_next_step_handler(message, edit_3reward_cost)

        def edit_3reward_cost(message):
            user_id = message.from_user.id
            reward_3cost = message.text.strip().lower()

            conn, cursor = get_user_db(user_id)
            cursor.execute(
                "UPDATE userdata SET  reward_3cost = ? WHERE id = "
                "(SELECT MAX(id) FROM userdata)",
                (reward_3cost, ),
            )
            conn.commit()
            conn.close()

            bot.send_message(user_id, "Отлично! Сколько львят "
                             "должна потратить ваша вторая "
                             "половинка, чтобы получить третью награду?")

            send_user_data(message)

        @bot.message_handler(commands=["help"])
        def help(message):
            user_id = message.from_user.id
            bot.send_message(user_id, "тут туториал")
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "да", callback_data="button9")
            button2 = telebot.types.InlineKeyboardButton(
                "нет", callback_data="button8")
            markup.add(button1, button2)
            bot.send_message(user_id, "Все еще запутаны? 🤔",
                             reply_markup=markup)

        @bot.message_handler(commands=["profile"])
        def profile(message):
            user_id = message.from_user.id
            conn, cursor = get_user_db(user_id)
            cursor.execute(get_data)
            user_data = cursor.fetchone()
            conn.close()
            if user_data:
                (
                    quser_name,
                    soulmate_name,
                    user_task,
                    user_2task,
                    user_3task,
                    task_cost,
                    task_2cost,
                    task_3cost,
                    user_reward,
                    reward_cost,
                    user_2reward,
                    reward_2cost,
                    user_3reward,
                    reward_3cost,
                    l_balance,
                ) = user_data

                response = (
                        f"💖{quser_name} и {soulmate_name}💖\n"
                        f"Ваши задания:\n"
                        f"1. {user_task} - за {task_cost} львят\n"
                        f"2. {user_2task} - за {task_2cost} львят\n"
                        f"3. {user_3task} - за {task_3cost} львят\n"
                        f"Ваши награды:\n"
                        f"1. {user_reward} - за {reward_cost} львят\n"
                        f"2. {user_2reward} - за {reward_2cost} львят\n"
                        f"3. {user_3reward} - за {reward_3cost} львят\n"
                        f"Баланс львят: {l_balance}")
            photo = "lions2.jpeg"
            file = open("./" + photo, "rb")
            bot.send_photo(user_id, file)
            bot.send_message(user_id, response)
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "да", callback_data="button1")
            button2 = telebot.types.InlineKeyboardButton(
                "нет", callback_data="button2")
            markup.add(button1, button2)
            bot.send_message(user_id, "want to edit?", reply_markup=markup)

        # ----------------------------------------------- #
        #                   random                        #
        #                                                 #
        #                                                 #
        #                                                 #
        # ----------------------------------------------- #

        tasks = [
            "Приготовьте специальный ужин для вашего партнера.",
            "Напишите любовное письмо.",
            "Испечь печенье или кексы.",
            "Посадите цветы в саду.",
            "Запланируйте неожиданное свидание.",
            "Организуйте романтический пикник.",
            "Занимайтесь всеми домашними делами в течение дня.",
            "Сделайте массаж стоп вашему партнеру.",
            "Напишите список вещей, которые вам нравятся в вашем партнере.",
            "Создайте альбом ваших любимых воспоминаний.",
            "Проведите день без гаджетов.",
            "Вымойте посуду.",
            "Уберите весь дом.",
            "Пропылесосьте все комнаты.",
            "Сходите за продуктами.",
            "Позаботьтесь о стирке.",
            "Уберите снег.",
            "Выгуляйте и ухаживайте за домашним питомцем.",
            "Умойте окна и зеркала.",
            "Настройте или почините компьютер.",
            "Вынесите мусор.",
            "Заберите детей из школы.",
            "Разберите вещи в шкафу.",
            "Завтрак в постели.",
        ]

        rewards = [
            "Запланируйте посещение художественной галереи.",
            "Попробуйте новый ресторан.",
            "Контроль над пультом ТВ на целый день.",
            "Устроить веселое чаепитие с плюшевыми игрушками.",
            "Прочитайте сказку перед сном с голосами персонажей.",
            "Прокатитесь на велосипеде в парке.",
            "Рисуйте и раскрашивайте вместе.",
            "Устройте киноночь с любимыми фильмами.",
            "Устроить пикник во дворе.",
            "Прогуляйтесь на природе и соберите листья или камни.",
            "Сыграйте в настольную или карточную игру.",
            "Устроить сессию рисования или искусства.",
            "Наблюдайте за закатом или восходом солнца вместе.",
            "Постройте научный эксперимент.",
            "Посетите музей или научный центр.",
            "Устроить караоке-вечер дома.",
            "Создайте вместе временную капсулу.",
            "Проведите спа-день с домашними масками.",
            "Посетите местное общественное событие.",
            "Прокатитесь верхом на лошади вместе.",
            "Проведите день на пляже.",
            "Сделайте короткую поездку в ближайший город.",
            "Запланируйте день на выбор вашего партнера.",
            "Сюрприз-подарок.",
            "Долгие, теплые объятия.",
            "День комплиментов.",
            "Неожиданное приключение.",
            "День, чтобы попробовать что-то новое.",
        ]

        @bot.message_handler(commands=["suggest"])
        def suggest(message):
            user_id = message.from_user.id
            # random_task = random.choice(tasks)
            # random_reward = random.choice(rewards)
            bot.send_message(
                user_id,
                f"Задания:\n"
                f"1. {random.choice(tasks)}\n"
                f"2. {random.choice(tasks)}\n"
                f"3. {random.choice(tasks)}\nНаграды:\n"
                f"1. {random.choice(rewards)}\n"
                f"2. {random.choice(rewards)}\n"
                f"3. {random.choice(rewards)}",
            )

        @bot.message_handler(commands=["share"])
        def share(message):
            user_id = message.from_user.id
            photo = "lions_share.jpeg"
            file = open("./" + photo, "rb")
            bot.send_photo(user_id, file)
            # terminal
            user = message.from_user
            user_id = user.id
            response = (f"{user_id}")
            bot.send_message(user_id, response)
            # terminal
            # myuuid = uuid.uuid4()
            # print('Your UUID is: ' + str(myuuid))

        @bot.message_handler(commands=["input"])
        def input_p(message):
            bot.send_message(
                message.chat.id, "Введите, пожалуйста, свой код")
            bot.register_next_step_handler(message, inputproccesing)

        def inputproccesing(message):
            try:
                user_id = message.from_user.id
                db_filename = message.text.strip().lower() + '.db'
                conn = sqlite3.connect(db_filename)
                cursor = conn.cursor()
                cursor.execute(get_data)

                user_data = cursor.fetchone()
                conn.close()
                if user_data:
                    (
                        quser_name,
                        soulmate_name,
                        user_task,
                        user_2task,
                        user_3task,
                        task_cost,
                        task_2cost,
                        task_3cost,
                        user_reward,
                        reward_cost,
                        user_2reward,
                        reward_2cost,
                        user_3reward,
                        reward_3cost,
                        l_balance,
                    ) = user_data

                    response = (
                        f"💖{quser_name} и {soulmate_name}💖\n"
                        f"Ваши задания:\n"
                        f"1. {user_task} - за {task_cost} львят\n"
                        f"2. {user_2task} - за {task_2cost} львят\n"
                        f"3. {user_3task} - за {task_3cost} львят\n"
                        f"Ваши награды:\n"
                        f"1. {user_reward} - за {reward_cost} львят\n"
                        f"2. {user_2reward} - за {reward_2cost} львят\n"
                        f"3. {user_3reward} - за {reward_3cost} львят\n"
                        f"Баланс львят: {l_balance}")
                bot.send_message(user_id, response)
                markup = telebot.types.InlineKeyboardMarkup()
                button1 = telebot.types.InlineKeyboardButton(
                    "да", callback_data="button1")
                button2 = telebot.types.InlineKeyboardButton(
                    "нет", callback_data="button2")
                markup.add(button1, button2)
                bot.send_message(user_id, "Хотите внести изменения?",
                                 reply_markup=markup)
            except Exception as e:
                bot.send_message(
                    message.chat.id,
                    f"An error occurred "
                    f"while searching the database: {str(e)}",
                )

        bot.infinity_polling(timeout=10, long_polling_timeout=5)

    # ----------------------------------------------- #
    except Exception as e:
        error_message = str(e)
        print(f"An error occurred: {error_message}")
        bot.send_message(me, f"An error occurred: {error_message}")
        bot.send_message(me, "restarting...")
        print(" Stopping the bot...")
        print("# ---------------------end((------------------------- #\n")
        bot.stop_polling()
        time.sleep(1)
