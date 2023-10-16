# ----------------------------------------------- #
# Project Name          : lions       			  #
# Author Name           : Lev Babushkin           #
# File Name             : main.py                 #
# Contact in telegram   : @levaau                 #
# ----------------------------------------------- #
import telebot
import sqlite3
from telebot import types
bot = telebot.TeleBot('6499881879:AAHslQDLXLNbNCM4zFhYMPEWiEHVibzgaA8')
# ----------------------------------------------- #
# MADE:SOLVE WITH EDITING INFO!!
# NEED: fix timeout=25, rewrite text, create /help, edit more rules and more

def get_user_db(user_id):
    conn = sqlite3.connect(f'{user_id}.db')
    cursor = conn.cursor()
    return conn, cursor

def create_user_table(user_id):
    conn, cursor = get_user_db(user_id)
    cursor.execute('''CREATE TABLE IF NOT EXISTS userdata
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      quser_name TEXT,
                      soulmate_name TEXT, user_task TEXT, task_cost INTEGER, user_reward TEXT, reward_cost INTEGER, l_balance INTEGER DEFAULT 0)''')#INTEGER DEFAULT 0
    conn.commit()
    conn.close()


@bot.message_handler(commands=['start'])
def greet_user(message):
    try:
        user_id = message.from_user.id
        conn, cursor = get_user_db(user_id)
        cursor.execute("SELECT quser_name, soulmate_name, user_task, task_cost, user_reward, reward_cost, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            quser_name, soulmate_name, user_task, task_cost, user_reward, reward_cost, l_balance = user_data
            response = f"Your name: {quser_name}\nYour soulmate name: {soulmate_name}\nYour task is: {user_task} - for {task_cost} lions\nYour reward is: {user_reward} - for {reward_cost} liond\nlions balance: {l_balance}"
        else:
            response = "I don't have your data yet. Please provide your information."
        bot.send_message(user_id, response)
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton("yes", callback_data='button1')
        button2 = telebot.types.InlineKeyboardButton("no", callback_data='button2')
        markup.add(button1, button2)
        bot.send_message(user_id, "Want to edit?", reply_markup=markup)
    except Exception:
        user_id = message.from_user.id
        create_user_table(user_id)
        bot.send_message(user_id, "Hello, I'm here to help your have fun! It's lions app!\nA small tutorial for you:")
        video = 'help.mp4'
        file = open('./' + video, 'rb')
        bot.send_video(message.chat.id, file)
        bot.send_message(user_id, "And let's begin!\nWhat's your name?")
        bot.register_next_step_handler(message, ask_quser_name)
        
def ask_quser_name(message):
    user_id = message.from_user.id
    quser_name = message.text.strip().lower()
    conn, cursor = get_user_db(user_id)
    cursor.execute("INSERT INTO userdata (quser_name, l_balance) VALUES (?, 0)", (quser_name,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Great! What's your soulmate's name?")
    bot.register_next_step_handler(message, ask_soulmate_name)

# Function to record the user's soulmate_name in the database
def ask_soulmate_name(message):
    user_id = message.from_user.id
    soulmate_name = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET soulmate_name = ? WHERE id = (SELECT MAX(id) FROM userdata)", (soulmate_name,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Now give me your task:")
    bot.register_next_step_handler(message, ask_user_task)

def ask_user_task(message):
    user_id = message.from_user.id
    user_task = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_task = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_task,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "What's the cost of the task?")
    bot.register_next_step_handler(message, ask_task_cost)

def ask_task_cost(message):
    user_id = message.from_user.id
    task_cost = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  task_cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (task_cost,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "How will you reward?")
    bot.register_next_step_handler(message, ask_reward)

def ask_reward(message):
    user_id = message.from_user.id
    user_reward = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_reward = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_reward,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "How much will it cost?")
    bot.register_next_step_handler(message, ask_reward_cost)

def ask_reward_cost(message):
    user_id = message.from_user.id
    reward_cost = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  reward_cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (reward_cost,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Thanks for sharing your information! Here's what I know about you:")
    send_user_data(message)

def send_user_data(message):
    user_id = message.from_user.id
    conn, cursor = get_user_db(user_id)
    cursor.execute("SELECT quser_name, soulmate_name, user_task, task_cost, user_reward, reward_cost, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        quser_name, soulmate_name, user_task, task_cost, user_reward, reward_cost, l_balance = user_data
        response = f"Your name: {quser_name}\nYour soulmate name: {soulmate_name}\nYour task is: {user_task} - for {task_cost} lions\nYour reward is: {user_reward} - for {reward_cost} lions\nLions balance: {l_balance}"
    else:
        response = "I don't have your data yet. Please provide your information."
    bot.send_message(user_id, response)
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("yes", callback_data='button1')
    button2 = telebot.types.InlineKeyboardButton("no", callback_data='button2')
    markup.add(button1, button2)
    bot.send_message(user_id, "Want to edit?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True) # main message
def callback_handler(call):
    user_id = call.from_user.id
    if call.data == 'button2':
        conn, cursor = get_user_db(user_id)
        cursor.execute("SELECT quser_name, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
        user_data = cursor.fetchone()
        if user_data:
            quser_name, l_balance = user_data
            markup = telebot.types.InlineKeyboardMarkup()
            button3 = telebot.types.InlineKeyboardButton("add", callback_data='button3')
            button4 = telebot.types.InlineKeyboardButton("remove", callback_data='button4')
            markup.row(button3, button4)
            button5 = telebot.types.InlineKeyboardButton("edit rules", callback_data='button5')
            button6 = telebot.types.InlineKeyboardButton("more", callback_data='button6')
            markup.row(button5, button6)
            photo = 'lions.png'
            file = open('./' + photo, 'rb')
            bot.send_message(call.message.chat.id, f"Hello, {quser_name}!\nlions balance: {l_balance}")#, reply_markup=markup)
            bot.send_photo(call.message.chat.id, file, reply_markup=markup)    
    elif call.data == 'button1':
        bot.send_message(user_id, "Okay, let's begin!\nWhat's your name?")
        bot.register_next_step_handler(call.message, edit_quser_name)
    elif call.data == 'button3':
        bot.send_message(call.message.chat.id, "How much?") #plus
        bot.register_next_step_handler(call.message, pluslions)
    elif call.data == 'button4':
        bot.send_message(call.message.chat.id, "How much?") #minus
        bot.register_next_step_handler(call.message, minuslions)
    elif call.data == 'button5': #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        bot.send_message(user_id, "Okay, let's begin!\nWhat's your name?")
        bot.register_next_step_handler(call.message, edit_quser_name)
    elif call.data == 'button6':
        bot.send_message(call.message.chat.id, "this is settings")
        bot.register_next_step_handler(call.message, more)

def minuslions(message):
    user_id = message.from_user.id
    conn, cursor = get_user_db(user_id)
    cursor.execute("SELECT l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
    user_data = cursor.fetchone()
    if user_data:
        l_balance, = user_data  # Unpack the value from the tuple
        l_balance_new = int(message.text.strip())
        l_balance -= l_balance_new
        cursor.execute("UPDATE userdata SET  l_balance = ? WHERE id = (SELECT MAX(id) FROM userdata)", (l_balance,))
        conn.commit()
        conn.close() #end!!!!
        conn, cursor = get_user_db(user_id)
        cursor.execute("SELECT quser_name, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
        user_data = cursor.fetchone()
        if user_data:
            quser_name, l_balance = user_data
            markup = telebot.types.InlineKeyboardMarkup()
            button3 = telebot.types.InlineKeyboardButton("add", callback_data='button3')
            button4 = telebot.types.InlineKeyboardButton("remove", callback_data='button4')
            markup.row(button3, button4)
            button5 = telebot.types.InlineKeyboardButton("edit rules", callback_data='button5')
            button6 = telebot.types.InlineKeyboardButton("more", callback_data='button6')
            markup.row(button5, button6)
            photo = 'lions.png'
            file = open('./' + photo, 'rb')
            bot.send_message(user_id, f"Hello, {quser_name}!\nlions balance: {l_balance}")#, reply_markup=markup)
            bot.send_photo(user_id, file, reply_markup=markup)
    else:
        bot.send_message(user_id, "Error: User data not found. Please make sure you have provided your information.")


def pluslions(message):
    user_id = message.from_user.id
    conn, cursor = get_user_db(user_id)
    cursor.execute("SELECT l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
    user_data = cursor.fetchone()
    if user_data:
        l_balance, = user_data  # Unpack the value from the tuple
        l_balance_new = int(message.text.strip())
        l_balance += l_balance_new
        cursor.execute("UPDATE userdata SET  l_balance = ? WHERE id = (SELECT MAX(id) FROM userdata)", (l_balance,))
        conn.commit()
        conn.close() #end!!!!
        conn, cursor = get_user_db(user_id)
        cursor.execute("SELECT quser_name, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
        user_data = cursor.fetchone()
        if user_data:
            quser_name, l_balance = user_data
            markup = telebot.types.InlineKeyboardMarkup()
            button3 = telebot.types.InlineKeyboardButton("add", callback_data='button3')
            button4 = telebot.types.InlineKeyboardButton("remove", callback_data='button4')
            markup.row(button3, button4)
            button5 = telebot.types.InlineKeyboardButton("edit rules", callback_data='button5')
            button6 = telebot.types.InlineKeyboardButton("more", callback_data='button6')
            markup.row(button5, button6)
            photo = 'lions.png'
            file = open('./' + photo, 'rb')
            bot.send_message(user_id, f"Hello, {quser_name}!\nlions balance: {l_balance}")#, reply_markup=markup)
            bot.send_photo(user_id, file, reply_markup=markup)
    else:
        bot.send_message(user_id, "Error: User data not found. Please make sure you have provided your information.")
def reversedlogin(message):
    #user_id = message.from_user.id
    bot.send_message(message, "Want to edit?")
def more(message):
    user_id = message.from_user.id

@bot.message_handler(commands=['start_edit_info'])
def start_edit_info(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "What's your name?")
    bot.register_next_step_handler(message, edit_quser_name)
def edit_quser_name(message):
    user_id = message.from_user.id
    quser_name = message.text.strip().lower()
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  quser_name = ? WHERE id = (SELECT MAX(id) FROM userdata)", (quser_name,))
    conn.commit()
    conn.close()
    bot.send_message(user_id, "Great! What's your soulmate's name?")
    bot.register_next_step_handler(message, edit_soulmate_name)
def edit_soulmate_name(message):
    user_id = message.from_user.id
    soulmate_name = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET soulmate_name = ? WHERE id = (SELECT MAX(id) FROM userdata)", (soulmate_name,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Now give me your task:")
    bot.register_next_step_handler(message, edit_user_task)

def edit_user_task(message):
    user_id = message.from_user.id
    user_task = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_task = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_task,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "What's the cost of the task?")
    bot.register_next_step_handler(message, edit_task_cost)

def edit_task_cost(message):
    user_id = message.from_user.id
    task_cost = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  task_cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (task_cost,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "How will you reward?")
    bot.register_next_step_handler(message, edit_reward)

def edit_reward(message):
    user_id = message.from_user.id
    user_reward = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_reward = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_reward,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "How much will it cost?")
    bot.register_next_step_handler(message, edit_reward_cost)

def edit_reward_cost(message):
    user_id = message.from_user.id
    reward_cost = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  reward_cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (reward_cost,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Thanks for sharing your information! Here's what I know about you:")
    send_user_data_edited(message)

def send_user_data_edited(message):
    user_id = message.from_user.id
    conn, cursor = get_user_db(user_id)
    cursor.execute("SELECT quser_name, soulmate_name, user_task, task_cost, user_reward, reward_cost, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        quser_name, soulmate_name, user_task, task_cost, user_reward, reward_cost, l_balance = user_data
        response = f"Your name: {quser_name}\nYour soulmate name: {soulmate_name}\nYour task is: {user_task} - for {task_cost} lions\nYour reward is: {user_reward} - for {reward_cost} lions\nLions balance: {l_balance}"
    else:
        response = "I don't have your data yet. Please provide your information."
    bot.send_message(user_id, response)
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("yes", callback_data='button1')
    button2 = telebot.types.InlineKeyboardButton("no", callback_data='button2')
    markup.add(button1, button2)
    bot.send_message(user_id, "Want to edit?", reply_markup=markup)
    

@bot.message_handler(commands=['wtf'])
def wtf(message):
    user_id = message.from_user.id
    conn, cursor = get_user_db(user_id)
    cursor.execute("SELECT quser_name, soulmate_name, user_task, task_cost, user_reward, reward_cost, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        quser_name, soulmate_name, user_task, task_cost, user_reward, reward_cost, l_balance = user_data
        response = f"Your name: {quser_name}\nYour soulmate name: {soulmate_name}\nYour task is: {user_task} - for {task_cost} lions\nYour reward is: {user_reward} - for {reward_cost} lions\nLions balance: {l_balance}"
    else:
        response = "I don't have your data yet. Please provide your information."
    bot.send_message(user_id, response)
        
bot.polling(non_stop=True)
