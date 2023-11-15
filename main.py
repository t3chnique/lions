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
# import subprocess
import json
from telebot import types
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')
me = os.getenv('ME')

bot = telebot.TeleBot(token)
# ----------------------------------------------- #

user_language = {}
# -----------------responce---------------------- #
with open("response.json", "r", encoding="utf-8") as file:
    response = json.load(file)

re = response

und = re["und"]
tasks_res = re["tasks"]
dlya = re["dlya"]
lions = re["lions"]
balance = re["balance"]
rewards_res = re["rewards"]
y = re["y"]
n = re["n"]
undr = re["undr"]
tasks_resr = re["tasksr"]
dlyar = re["dlyar"]
lionsr = re["lionsr"]
rewardsr = re["rewardsr"]
balancer = re["balancer"]
yr = ["yr"]
# -----------------responce---------------------- #

# -----------------strings_en---------------------- #
with open("strings_en.json", "r", encoding="utf-8") as file:
    strings_en = json.load(file)

se = strings_en

tuten1 = se["tut"]

# -----------------strings_en---------------------- #

# -----------------strings_ru---------------------- #
with open("strings_ru.json", "r", encoding="utf-8") as file:
    strings_ru = json.load(file)

sr = strings_ru

tuter1 = sr["tut"]

# -----------------strings_ru---------------------- #


def exit_gracefully(signal, frame):
    print(" Stopping the bot...")
    print("# ---------------------end((------------------------- #\n")
    bot.send_message(me, "shutting down...")
    sys.exit(0)


signal.signal(signal.SIGINT, exit_gracefully)

get_data = strings_en["get_data"]


while True:
    try:
        # ----------------------------------------------- #
        # MADE:

        # fix terminal, make a protection of user_id

        # NEED: delete useless messages, add custom font, allow 2
        # users to work on the same database. make a real donation request,
        # design repeater, make suggest button in registration and editting
        # X-step tutorial with buttons
        print("\n# ---------------------start main en---------------------- #")
        print("hello, this is a small addition to the bot")
        bot.send_message(me, "turning on...")

        @bot.message_handler(commands=["search"])
        def search(message):
            bot.send_message(
                message.chat.id, "Please enter the name "
                "of the SQL database file.")
            welcome_message = strings_en["welcome"]
            bot.send_message(
                message.chat.id, welcome_message)
            bot.register_next_step_handler(message, search_database)

        # @bot.message_handler(commands=["diepls"])
        # def diepls(message):
            # os._exit(0)

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
                        f"💖{quser_name} {und} {soulmate_name}💖\n"
                        f"{tasks_res}:\n"
                        f"1. {user_task} - {dlya} {task_cost} {lions}\n"
                        f"2. {user_2task} - {dlya} {task_2cost} {lions}\n"
                        f"3. {user_3task} - {dlya} {task_3cost} {lions}\n"
                        f"{rewards_res}:\n"
                        f"1. {user_reward} - {dlya} {reward_cost} {lions}\n"
                        f"2. {user_2reward} - {dlya} {reward_2cost} {lions}\n"
                        f"3. {user_3reward} - {dlya} {reward_3cost} {lions}\n"
                        f"{balance}: {l_balance}")
                else:
                    response = "I don't have your data yet. "
                    "Please provide your information."
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
                            l_balance INTEGER DEFAULT 0, lang TEXT)""")
            conn.commit()
            conn.close()

        def delete_message_call(call):
            for i in range(0, 50):
                bot.delete_message(call.message.chat.id,
                                   call.message.message_id-i)

        def delete_message_message(message):
            for i in range(0, 50):
                bot.delete_message(message.chat.id, message.message_id-i)

        @bot.message_handler(commands=["start"])
        def language(message):
            user_id = message.from_user.id
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "english", callback_data="en")
            button2 = telebot.types.InlineKeyboardButton(
                "russian", callback_data="ru")
            markup.add(button1, button2)
            bot.send_message(user_id, "hi, choose you language first",
                             reply_markup=markup)

        # @bot.message_handler(commands=["start"])
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
                    if user_id in user_language:
                        language = user_language[user_id]
                    else:
                        language = "en"
                        user_language[user_id] = language
                    if language.lower() == "en":
                        response = (
                            f"💖{quser_name} {und} {soulmate_name}💖\n"
                            f"{tasks_res}:\n"
                            f"1. {user_task} - {dlya} {task_cost} {lions}\n"
                            f"2. {user_2task} - {dlya} {task_2cost} {lions}\n"
                            f"3. {user_3task} - {dlya} {task_3cost} {lions}\n"
                            f"{rewards_res}:\n"
                            f"1. {user_reward} - {dlya} "
                            f"{reward_cost} {lions}\n"
                            f"2. {user_2reward} - {dlya} "
                            f"{reward_2cost} {lions}\n"
                            f"3. {user_3reward} - {dlya} "
                            f"{reward_3cost} {lions}\n"
                            f"{balance}: {l_balance}")
                    else:
                        response = (
                            f"💖{quser_name} {undr} {soulmate_name}💖\n"
                            f"{tasks_resr}:\n"
                            f"1. {user_task} - {dlyar} {task_cost} {lionsr}\n"
                            f"2. {user_2task} - {dlyar} "
                            f"{task_2cost} {lionsr}\n"
                            f"3. {user_3task} - {dlyar} "
                            f"{task_3cost} {lionsr}\n"
                            f"{rewards_res}:\n"
                            f"1. {user_reward} - {dlyar} "
                            f"{reward_cost} {lionsr}\n"
                            f"2. {user_2reward} - {dlyar} "
                            f"{reward_2cost} {lionsr}\n"
                            f"3. {user_3reward} - {dlyar} "
                            f"{reward_3cost} {lionsr}\n"
                            f"{balancer}: {l_balance}")
                else:
                    response = "I don't have your data yet. "
                    "Please provide your information."
                photo = "lions2.jpeg"
                file = open("./" + photo, "rb")
                bot.send_photo(user_id, file)
                bot.send_message(user_id, response)
                markup = telebot.types.InlineKeyboardMarkup()
                button1 = telebot.types.InlineKeyboardButton(
                    f"{y}", callback_data="button1")
                button2 = telebot.types.InlineKeyboardButton(
                    f"{n}", callback_data="button2")
                markup.add(button1, button2)
                bot.send_message(user_id, "want to edit?", reply_markup=markup)
            except Exception:
                user_id = message.from_user.id
                create_user_table(user_id)
                markup = telebot.types.InlineKeyboardMarkup()
                button1 = telebot.types.InlineKeyboardButton(
                    "next", callback_data="tut1")
                markup.add(button1)
                photo = "lions_share.jpeg"
                file = open("./" + photo, "rb")
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = tuten1
                else:
                    response = tuter1
                bot.send_photo(user_id, file, caption=response,
                               reply_markup=markup)

        def tutorial2(message):
            user_id = message.from_user.id
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "next", callback_data="tut2")
            markup.add(button1)
            photo = "lions_share.jpeg"
            file = open("./" + photo, "rb")
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["tut1"]
            else:
                response = sr["tut1"]
            bot.send_photo(user_id, file, caption=response,
                           reply_markup=markup)

        def tutorial3(message):
            user_id = message.from_user.id
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "next", callback_data="tut3")
            markup.add(button1)
            photo = "lions_share.jpeg"
            file = open("./" + photo, "rb")
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["tut2"]
            else:
                response = sr["tut2"]
            bot.send_photo(user_id, file, caption=response,
                           reply_markup=markup)

        def tutorial4(message):
            user_id = message.from_user.id
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "next", callback_data="tut4")
            markup.add(button1)
            photo = "lions_share.jpeg"
            file = open("./" + photo, "rb")
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["tut3"]
            else:
                response = sr["tut3"]
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
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["s_name"]
            else:
                response = sr["s_name"]
            bot.send_message(
                user_id, response)
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

            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["1_task"]
            else:
                response = sr["1_task"]
            bot.send_message(
                user_id, response)
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
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["1_cost"]
            else:
                response = sr["1_cost"]
            bot.send_message(
                user_id, response)
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
                "no", callback_data="button10")
            button2 = telebot.types.InlineKeyboardButton(
                "yes", callback_data="button11")
            markup.add(button1, button2)
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["2_task"]
            else:
                response = sr["2_task"]
            bot.send_message(
                user_id, response, reply_markup=markup)

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
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["2_cost"]
            else:
                response = sr["2_cost"]
            bot.send_message(
                user_id, response)
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
                "no", callback_data="button10")
            button2 = telebot.types.InlineKeyboardButton(
                "yes", callback_data="button12")
            markup.add(button1, button2)
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["3_task"]
            else:
                response = sr["3_task"]
            bot.send_message(
                user_id, response, reply_markup=markup)

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
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["3_cost"]
            else:
                response = sr["3_cost"]
            bot.send_message(
                user_id, response)
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

            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["1_reward"]
            else:
                response = sr["1_reward"]
            bot.send_message(
                user_id, response)
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

            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["1_rcost"]
            else:
                response = sr["1_rcost"]
            bot.send_message(
                user_id, response)
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
                "no", callback_data="button15")
            button2 = telebot.types.InlineKeyboardButton(
                "yes", callback_data="button14")
            markup.add(button1, button2)
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["2_reward"]
            else:
                response = sr["2_reward"]
            bot.send_message(
                user_id, response, reply_markup=markup)

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

            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["2_rcost"]
            else:
                response = sr["2_rcost"]
            bot.send_message(
                user_id, response)
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
                "no", callback_data="button15")
            button2 = telebot.types.InlineKeyboardButton(
                "yes", callback_data="button17")
            markup.add(button1, button2)
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["3_reward"]
            else:
                response = sr["3_reward"]
            bot.send_message(
                user_id, response, reply_markup=markup)

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

            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["3_rcost"]
            else:
                response = sr["3_rcost"]
            bot.send_message(
                user_id, response)
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

            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                response = se["thanks"]
            else:
                response = sr["thanks"]
            bot.send_message(
                user_id, response)
            send_user_data(message)

        def send_user_data(call):
            user_id = call.from_user.id
            conn, cursor = get_user_db(user_id)
            cursor.execute(get_data)
            user_data = cursor.fetchone()
            conn.close()
            if user_data:
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
                    if user_id in user_language:
                        language = user_language[user_id]
                    else:
                        language = "en"
                        user_language[user_id] = language
                    if language.lower() == "en":
                        response = (
                            f"💖{quser_name} {und} {soulmate_name}💖\n"
                            f"{tasks_res}:\n"
                            f"1. {user_task} - {dlya} {task_cost} {lions}\n"
                            f"2. {user_2task} - {dlya} {task_2cost} {lions}\n"
                            f"3. {user_3task} - {dlya} {task_3cost} {lions}\n"
                            f"{rewards_res}:\n"
                            f"1. {user_reward} - {dlya} "
                            f"{reward_cost} {lions}\n"
                            f"2. {user_2reward} - {dlya} "
                            f"{reward_2cost} {lions}\n"
                            f"3. {user_3reward} - {dlya} "
                            f"{reward_3cost} {lions}\n"
                            f"{balance}: {l_balance}")
                    else:
                        response = (
                            f"💖{quser_name} {undr} {soulmate_name}💖\n"
                            f"{tasks_resr}:\n"
                            f"1. {user_task} - {dlyar} {task_cost} {lionsr}\n"
                            f"2. {user_2task} - {dlyar} "
                            f"{task_2cost} {lionsr}\n"
                            f"3. {user_3task} - {dlyar} "
                            f"{task_3cost} {lionsr}\n"
                            f"{rewards_res}:\n"
                            f"1. {user_reward} - {dlyar} "
                            f"{reward_cost} {lionsr}\n"
                            f"2. {user_2reward} - {dlyar} "
                            f"{reward_2cost} {lionsr}\n"
                            f"3. {user_3reward} - {dlyar} "
                            f"{reward_3cost} {lionsr}\n"
                            f"{balancer}: {l_balance}")
            else:
                response = (
                    "I don't have your data yet. "
                    "Please provide your information."
                )
            bot.send_message(user_id, response)
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                f"{y}", callback_data="button1")
            button2 = telebot.types.InlineKeyboardButton(
                f"{n}", callback_data="button2")
            markup.add(button1, button2)
            bot.send_message(user_id, "Want to edit?", reply_markup=markup)
            delete_message_call(call)

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
            if user_id in user_language:
                language = user_language[user_id]
            else:
                language = "en"
                user_language[user_id] = language
            if language.lower() == "en":
                markup = telebot.types.InlineKeyboardMarkup()
                button3 = telebot.types.InlineKeyboardButton(
                    "add", callback_data="button3")
                button4 = telebot.types.InlineKeyboardButton(
                    "remove", callback_data="button4")
                markup.row(button3, button4)
                button5 = telebot.types.InlineKeyboardButton(
                    "edit rules", callback_data="button5")
                button6 = telebot.types.InlineKeyboardButton(
                    "more", callback_data="button6")
                markup.row(button5, button6)
                photo = "lions.png"
                file = open("./" + photo, "rb")
                try:
                    bot.send_message(call.message.chat.id,
                                     f"Hello, {quser_name}!\n🦁: {l_balance}")
                    bot.send_photo(call.message.chat.id, file,
                                   reply_markup=markup)
                except Exception:
                    bot.send_message(call.chat.id,
                                     f"Hello, {quser_name}!\n🦁: {l_balance}")
                    bot.send_photo(call.chat.id, file, reply_markup=markup)
            else:
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
                    bot.send_photo(call.message.chat.id, file,
                                   reply_markup=markup)
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
            elif call.data == "button5":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["name"]
                else:
                    response = sr["name"]
                bot.send_message(user_id, response)
                bot.register_next_step_handler(call.message, edit_quser_name)
            elif call.data == "button1":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["name"]
                else:
                    response = sr["name"]
                bot.send_message(user_id, response)
                bot.register_next_step_handler(call.message, edit_quser_name)
            elif call.data == "button3":
                bot.send_message(call.message.chat.id, "How much?")  # plus
                bot.register_next_step_handler(call.message, pluslions)
            elif call.data == "button4":
                bot.send_message(call.message.chat.id, "How much?")  # minus
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
                delete_message_call(call)
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
                delete_message_call(call)
            elif call.data == "button10":  # same with 13
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["1_reward"]
                else:
                    response = sr["1_reward"]
                bot.send_message(
                    user_id, response)
                bot.register_next_step_handler(call.message, ask_reward)
            elif call.data == "button11":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["e2_task"]
                else:
                    response = sr["e2_task"]
                bot.send_message(
                    user_id, response)
                bot.register_next_step_handler(call.message, ask_user_2task)
            elif call.data == "button12":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["e3_task"]
                else:
                    response = sr["e3_task"]
                bot.send_message(
                    user_id, response)
                bot.register_next_step_handler(call.message, ask_user_3task)
            elif call.data == "button14":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["e2_reward"]
                else:
                    response = sr["e2_reward"]
                bot.send_message(
                    user_id, response)
                bot.register_next_step_handler(call.message, ask_2reward)
            elif call.data == "button15":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["thanks"]
                else:
                    response = sr["thanks"]
                bot.send_message(
                    user_id, response)
                send_user_data(call)
            elif call.data == "button17":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["e3_reward"]
                else:
                    response = sr["e3_reward"]
                bot.send_message(
                    user_id, response)
                bot.register_next_step_handler(call.message, ask_3reward)
            elif call.data == "button18":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["1_reward"]
                else:
                    response = sr["1_reward"]
                bot.send_message(
                    user_id, response)
                bot.register_next_step_handler(call.message, edit_reward)
            elif call.data == "button19":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["e2_task"]
                else:
                    response = sr["e2_task"]
                bot.send_message(
                    user_id, response)
                bot.register_next_step_handler(call.message, edit_user_2task)
            elif call.data == "button20":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["e3_task"]
                else:
                    response = sr["e3_task"]
                bot.send_message(
                    user_id, response)
                bot.register_next_step_handler(call.message, edit_user_3task)
            elif call.data == "button13":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["e2_reward"]
                else:
                    response = sr["e2_reward"]
                bot.send_message(
                    user_id, response)
                bot.register_next_step_handler(call.message, ask_2reward)
            elif call.data == "button16":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["e3_reward"]
                else:
                    response = sr["e3_reward"]
                bot.send_message(
                    user_id, response)
                bot.register_next_step_handler(call.message, edit_3reward)
            elif call.data == "tut1":
                tutorial2(call)
            elif call.data == "tut2":
                tutorial3(call)
            elif call.data == "tut3":
                tutorial4(call)
            elif call.data == "tut4":
                if user_id in user_language:
                    language = user_language[user_id]
                else:
                    language = "en"
                    user_language[user_id] = language
                if language.lower() == "en":
                    response = se["name"]
                else:
                    response = sr["name"]
                bot.send_message(user_id, response)
                bot.register_next_step_handler(call.message, ask_quser_name)
            elif call.data == "en":
                user_language[user_id] = 'en'
                bot.send_message(user_id, "Language set to English.")
                greet_user(call)
            elif call.data == "ru":
                user_language[user_id] = 'ru'
                bot.send_message(user_id, "Язык установлен на русский.")
                greet_user(call)

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
                delete_message_message(message)
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
                delete_message_message(message)
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
            bot.send_message(user_id,
                             "To get started, please tell me your name")
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
            bot.send_message(
                user_id, "Great! Now, I'd like to know your soulmate's name")
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

            bot.send_message(
                user_id,
                "Thank you! What's the first task you'd "
                "like to create for your soulmate?",
            )
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

            bot.send_message(
                user_id,
                "Wonderful! How many lions should your soulmate "
                "earn for completing the first task?",
            )

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
                "no", callback_data="button18")
            button2 = telebot.types.InlineKeyboardButton(
                "yes", callback_data="button19")
            markup.add(button1, button2)
            bot.send_message(
                user_id,
                "Would you like to add a second task for your soulmate?",
                reply_markup=markup,
            )

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
            bot.send_message(
                user_id,
                "Excellent choice! How many lions should your "
                "soulmate earn for completing the second task?",
            )
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
                "no", callback_data="button18")
            button2 = telebot.types.InlineKeyboardButton(
                "yes", callback_data="button20")
            markup.add(button1, button2)
            bot.send_message(
                message.chat.id,
                "Would you like to add a third task for your soulmate?",
                reply_markup=markup,
            )

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
            bot.send_message(
                user_id,
                "Perfect! How many lions should your soulmate earn "
                "for completing the third task?",
            )
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

            bot.send_message(
                user_id,
                "Now, let's talk about the rewards. What's the "
                "first reward you'd like to offer in exchange for lions?",
            )
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

            bot.send_message(
                user_id,
                "Terrific! How many lions should your soulmate "
                "spend to claim the first reward?",
            )
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
            bot.send_message(
                message.chat.id,
                "Would you like to add a second reward for your soulmate?",
                reply_markup=markup,
            )

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

            bot.send_message(
                user_id,
                "Great! How many lions should your soulmate "
                "spend to claim the second reward?",
            )
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
                "no", callback_data="button15")
            button2 = telebot.types.InlineKeyboardButton(
                "yes", callback_data="button16")
            markup.add(button1, button2)
            bot.send_message(
                message.chat.id,
                "Would you like to add a third reward for your soulmate?",
                reply_markup=markup,
            )

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

            bot.send_message(
                user_id,
                "Awesome! How many lions should your soulmate "
                "spend to claim the third reward?",
            )
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

            bot.send_message(
                user_id,
                "Thanks for sharing your information! "
                "Here's what I know about you:",
            )
            send_user_data(message)

        @bot.message_handler(commands=["help"])
        def help(message):
            user_id = message.from_user.id
            bot.send_message(
                user_id,
                "Hi there! Here's how Love & Lions works:\n"
                "You create tasks and rewards for your soulmate, "
                "assign them a lion value, and then they complete "
                "tasks to earn lions. These lions can be spent to "
                "claim the rewards you've set up. It's all about "
                "showing appreciation!\nThe video tutorial can be "
                "found below 🤗",
            )
            video = "help.mp4"
            file = open("./" + video, "rb")
            bot.send_video(message.chat.id, file)
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                "yes", callback_data="button9")
            button2 = telebot.types.InlineKeyboardButton(
                "no", callback_data="button8")
            markup.add(button1, button2)
            bot.send_message(user_id, "still confusing?", reply_markup=markup)

        @bot.message_handler(commands=["profile"])
        def profile(message):
            user_id = message.from_user.id
            conn, cursor = get_user_db(user_id)
            cursor.execute(get_data)
            user_data = cursor.fetchone()
            conn.close()
            if user_data:
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
                        f"💖{quser_name} {und} {soulmate_name}💖\n"
                        f"{tasks_res}:\n"
                        f"1. {user_task} - {dlya} {task_cost} {lions}\n"
                        f"2. {user_2task} - {dlya} {task_2cost} {lions}\n"
                        f"3. {user_3task} - {dlya} {task_3cost} {lions}\n"
                        f"{rewards_res}:\n"
                        f"1. {user_reward} - {dlya} {reward_cost} {lions}\n"
                        f"2. {user_2reward} - {dlya} {reward_2cost} {lions}\n"
                        f"3. {user_3reward} - {dlya} {reward_3cost} {lions}\n"
                        f"{balance}: {l_balance}")
            else:
                response = (
                    "I don't have your data yet. "
                    "Please provide your information."
                )
            photo = "lions2.jpeg"
            file = open("./" + photo, "rb")
            bot.send_photo(user_id, file)
            bot.send_message(user_id, response)
            markup = telebot.types.InlineKeyboardMarkup()
            button1 = telebot.types.InlineKeyboardButton(
                f"{y}", callback_data="button1")
            button2 = telebot.types.InlineKeyboardButton(
                f"{n}", callback_data="button2")
            markup.add(button1, button2)
            bot.send_message(user_id, "want to edit?", reply_markup=markup)

        # ----------------------------------------------- #
        #                   random                        #
        #                                                 #
        #                                                 #
        #                                                 #
        # ----------------------------------------------- #

        tasks = [
            "Cook a special dinner for your partner.",
            "Write a love letter.",
            "Learn a new dance or song.",
            "Bake cookies or cupcakes.",
            "Plant flowers in the garden.",
            "Plan a special birthday surprise.",
            "Plan a surprise date night.",
            "Organize a romantic picnic.",
            "Take care of all the household chores for a day.",
            "Give your partner a foot massage.",
            "Watch your partner's favorite movie.",
            "Write a list of things you love about your partner.",
            "Create a scrapbook of your favorite memories.",
            "Plan a game night at home.",
            "Have a technology-free day.",
            "Plan a spa day at home.",
            "Wash and dry the dishes.",
            "Clean the entire house.",
            "Vacuum all the rooms.",
            "Do the grocery shopping.",
            "Take care of the laundry.",
            "Shovel snow from the driveway.",
            "Walk and groom the family pet.",
            "Clean the windows and mirrors.",
            "Set up or fix a computer.",
            "Take out the trash.",
            "Get the kids from school.",
            "Organize the closet.",
        ]

        rewards = [
            "Plan a visit to an art gallery.",
            "Try a new restaurant.",
            "Breakfast in bed.",
            "Control of the TV remote for a day.",
            "Have a fun tea party with stuffed animals.",
            "Read a bedtime story with character voices.",
            "Go on a bike ride in the park.",
            "Draw and color together.",
            "Have a movie night with your favorite films.",
            "Have a picnic in the backyard.",
            "Take a nature walk and collect leaves or rocks.",
            "Play a board game or card game.",
            "Have a painting or art session.",
            "Watch the sunset or sunrise together.",
            "Build a science experiment.",
            "Explore a museum or science center.",
            "Have a karaoke night at home.",
            "Make a time capsule together.",
            "Have a spa day with homemade facials.",
            "Attend a local community event.",
            "Go horseback riding together.",
            "Have a day at the beach.",
            "Take a day trip to a nearby town.",
            "Plan a day of your partners choice.",
            "A surprise gift",
            "A long, warm hug.",
            "A day of compliments.",
            "A surprise adventure.",
            "A day to try something new.",
        ]

        @bot.message_handler(commands=["suggest"])
        def suggest(message):
            user_id = message.from_user.id
            # random_task = random.choice(tasks)
            # random_reward = random.choice(rewards)
            bot.send_message(
                user_id,
                f"Tasks:\n"
                f"1. {random.choice(tasks)}\n"
                f"2. {random.choice(tasks)}\n"
                f"3. {random.choice(tasks)}\nRewards:\n"
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
                message.chat.id, "Please enter your code")
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
                        f"💖{quser_name} {und} {soulmate_name}💖\n"
                        f"{tasks_res}:\n"
                        f"1. {user_task} - {dlya} {task_cost} {lions}\n"
                        f"2. {user_2task} - {dlya} {task_2cost} {lions}\n"
                        f"3. {user_3task} - {dlya} {task_3cost} {lions}\n"
                        f"{rewards_res}:\n"
                        f"1. {user_reward} - {dlya} {reward_cost} {lions}\n"
                        f"2. {user_2reward} - {dlya} {reward_2cost} {lions}\n"
                        f"3. {user_3reward} - {dlya} {reward_3cost} {lions}\n"
                        f"{balance}: {l_balance}")
                else:
                    response = "I don't have your data yet. "
                    "Please provide your information."
                bot.send_message(user_id, response)
                markup = telebot.types.InlineKeyboardMarkup()
                button1 = telebot.types.InlineKeyboardButton(
                    f"{y}", callback_data="button1")
                button2 = telebot.types.InlineKeyboardButton(
                    f"{n}", callback_data="button2")
                markup.add(button1, button2)
                bot.send_message(user_id, "Want to edit?", reply_markup=markup)
            except Exception as e:
                bot.send_message(
                    message.chat.id,
                    f"An error occurred "
                    f"while searching the database: {str(e)}",
                )

        bot.infinity_polling(timeout=10, long_polling_timeout=5)
        # if __name__ == "__main__":
        # bot.polling(none_stop=True)

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
