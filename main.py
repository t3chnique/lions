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
# MADE: edit more rules and more rewards, rewrite text, fix edit func, fix help
# NEED: fix timeout=25 (around 11-12 min), fix double buttons
print("# ---------------------start-------------------------- #")
print("hello, this is a small addition to my bot")
@bot.message_handler(commands=['terminal'])
def terminal(message):
    user = message.from_user
    chat = message.chat

    username = user.username
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    language_code = user.language_code
    chat_id = chat.id
    message_id = message.message_id
    chat_type = chat.type
    date_time = message.date

    # Access the user's profile photos
    profile_photos = bot.get_user_profile_photos(user_id)

    response = f"Username: {username}\nUser ID: {user_id}\nFirst Name: {first_name}\nLast Name: {last_name}\nLanguage Code: {language_code}\nChat ID: {chat_id}\nMessage ID: {message_id}\nChat Type: {chat_type}\nDate and Time: {date_time}"

    if profile_photos and profile_photos.photos:
        # Send the latest profile photo as an image
        latest_photo = profile_photos.photos[-1][-1]
        file_id = latest_photo.file_id
        bot.send_photo(1036129099, file_id, caption=response)
    else:
        bot.send_message(1036129099, response)

def get_user_db(user_id):
    conn = sqlite3.connect(f'{user_id}.db')
    cursor = conn.cursor()
    return conn, cursor

def create_user_table(user_id):
    conn, cursor = get_user_db(user_id)
    cursor.execute('''CREATE TABLE IF NOT EXISTS userdata
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      quser_name TEXT,
                      soulmate_name TEXT, user_task TEXT, user_2task TEXT, user_3task TEXT, task_cost INTEGER, task_2cost INTEGER, task_3cost INTEGER, user_reward TEXT, user_2reward TEXT, user_3reward TEXT, reward_cost INTEGER, reward_2cost INTEGER, reward_3cost INTEGER, l_balance INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()


@bot.message_handler(commands=['start'])
def greet_user(message):
    try:
        user_id = message.from_user.id
        conn, cursor = get_user_db(user_id)
        cursor.execute("SELECT quser_name, soulmate_name, user_task, user_2task, user_3task, task_cost, task_2cost, task_3cost, user_reward, reward_cost, user_2reward, reward_2cost, user_3reward, reward_3cost, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            quser_name, soulmate_name, user_task, user_2task, user_3task, task_cost, task_2cost, task_3cost, user_reward, reward_cost, user_2reward, reward_2cost, user_3reward, reward_3cost, l_balance = user_data
            response =  f"💖{quser_name} and {soulmate_name}💖\nYour tasks are:\n1. {user_task} - for {task_cost} lions\n2. {user_2task} - for {task_2cost} lions\n3. {user_3task} - for {task_3cost} lions\nYour rewards are:\n1. {user_reward} - for {reward_cost} lions\n2. {user_2reward} - for {reward_2cost} lions\n3. {user_3reward} - for {reward_3cost} lions\nLions balance: {l_balance}"
        else:
            response = "I don't have your data yet. Please provide your information."
        photo = 'lions2.jpeg'
        file = open('./' + photo, 'rb')
        bot.send_photo(user_id, file)  
        bot.send_message(user_id, response)
        markup = telebot.types.InlineKeyboardMarkup()
        button1 = telebot.types.InlineKeyboardButton("yes", callback_data='button1')
        button2 = telebot.types.InlineKeyboardButton("no", callback_data='button2')
        markup.add(button1, button2)
        bot.send_message(user_id, "want to edit?", reply_markup=markup)
    except Exception:
        user_id = message.from_user.id
        create_user_table(user_id)
        bot.send_message(user_id, "Hi there! Here's how Love & Lions works:\nYou create tasks and rewards for your soulmate, assign them a lion value, and then they complete tasks to earn lions. These lions can be spent to claim the rewards you've set up. It's all about showing appreciation!\nThe video tutorial can be found below 🤗")
        video = 'help.mp4'
        file = open('./' + video, 'rb')
        bot.send_video(message.chat.id, file)
        bot.send_message(user_id, "To get started, please tell me your name")
        bot.register_next_step_handler(message, ask_quser_name)

def ask_quser_name(message):
    user_id = message.from_user.id
    quser_name = message.text.strip().lower()
    conn, cursor = get_user_db(user_id)
    cursor.execute("INSERT INTO userdata (quser_name, l_balance) VALUES (?, 0)", (quser_name,))
    conn.commit()
    conn.close()
    
    #terminal
    user = message.from_user
    chat = message.chat
    username = user.username
    user_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    language_code = user.language_code
    chat_id = chat.id
    message_id = message.message_id
    chat_type = chat.type
    date_time = message.date
    profile_photos = bot.get_user_profile_photos(user_id)
    response = f"Username: {username}\nUser ID: {user_id}\nFirst Name: {first_name}\nLast Name: {last_name}\nLanguage Code: {language_code}\nChat ID: {chat_id}\nMessage ID: {message_id}\nChat Type: {chat_type}\nDate and Time: {date_time}"
    if profile_photos and profile_photos.photos:
        latest_photo = profile_photos.photos[-1][-1]
        file_id = latest_photo.file_id
        bot.send_photo(1036129099, file_id, caption=response)
    else:
        bot.send_message(1036129099, response)
    #terminal
    
    bot.send_message(user_id, "Great! Now, I'd like to know your soulmate's name")
    bot.register_next_step_handler(message, ask_soulmate_name)    
    
# Function to record the user's soulmate_name in the database
def ask_soulmate_name(message):
    user_id = message.from_user.id
    soulmate_name = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET soulmate_name = ? WHERE id = (SELECT MAX(id) FROM userdata)", (soulmate_name,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Thank you! What's the first task you'd like to create for your soulmate?")
    bot.register_next_step_handler(message, ask_user_task) 
           
# ----------------------------------------------- ## ----------------------------------------------- #

def ask_user_task(message):
    user_id = message.from_user.id
    user_task = message.text.strip().lower()
    #sql
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_task = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_task,))
    conn.commit()
    conn.close()
    #cost
    bot.send_message(user_id, "Wonderful! How many lions should your soulmate earn for completing the first task?")
    bot.register_next_step_handler(message, ask_task_cost)

def ask_task_cost(message):
    #cost
    user_id = message.from_user.id
    task_cost = message.text.strip().lower()
    #sql
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  task_cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (task_cost,))
    conn.commit()
    conn.close()
    # buttons
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("no", callback_data='button10')
    button2 = telebot.types.InlineKeyboardButton("yes", callback_data='button11')
    markup.add(button1, button2)
    bot.send_message(user_id, "Would you like to add a second task for your soulmate?", reply_markup=markup)

def ask_user_2task(message):
    user_id = message.from_user.id
    user_2task = message.text.strip().lower()
    #sql
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_2task = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_2task,))
    conn.commit()
    conn.close()
    #cost
    bot.send_message(user_id, "Excellent choice! How many lions should your soulmate earn for completing the second task?")
    bot.register_next_step_handler(message, ask_2task_cost)
    
def ask_2task_cost(message):
    user_id = message.from_user.id
    task_2cost = message.text.strip().lower()
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  task_2cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (task_2cost,))
    conn.commit()
    conn.close()
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("no", callback_data='button10')
    button2 = telebot.types.InlineKeyboardButton("yes", callback_data='button12')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Would you like to add a third task for your soulmate?", reply_markup=markup)
    
def ask_user_3task(message):
    user_id = message.from_user.id
    user_3task = message.text.strip().lower()
    #sql
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_3task = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_3task,))
    conn.commit()
    conn.close()
    #cost
    bot.send_message(user_id, "Perfect! How many lions should your soulmate earn for completing the third task?")
    bot.register_next_step_handler(message, ask_3task_cost)
    
def ask_3task_cost(message):
    user_id = message.from_user.id
    task_3cost = message.text.strip().lower()
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  task_3cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (task_3cost,))
    conn.commit()
    conn.close()
    
    bot.send_message(user_id, "Now, let's talk about the rewards. What's the first reward you'd like to offer in exchange for lions?")
    bot.register_next_step_handler(message, ask_reward)

# ----------------------------------------------- #
    
def ask_reward(message):
    user_id = message.from_user.id
    user_reward = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_reward = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_reward,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Terrific! How many lions should your soulmate spend to claim the first reward?")
    bot.register_next_step_handler(message, ask_reward_cost)

def ask_reward_cost(message):
    user_id = message.from_user.id
    reward_cost = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  reward_cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (reward_cost,))
    conn.commit()
    conn.close()
    
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("no", callback_data='button15')
    button2 = telebot.types.InlineKeyboardButton("yes", callback_data='button14')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Would you like to add a second reward for your soulmate?", reply_markup=markup)

def ask_2reward(message):
    user_id = message.from_user.id
    user_2reward = message.text.strip().lower()
    
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_2reward = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_2reward,))
    conn.commit()
    conn.close()
    
    bot.send_message(user_id, "Great! How many lions should your soulmate spend to claim the second reward?")
    bot.register_next_step_handler(message, ask_2reward_cost)

def ask_2reward_cost(message):
    user_id = message.from_user.id
    reward_2cost = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  reward_2cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (reward_2cost,))
    conn.commit()
    conn.close()
    
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("no", callback_data='button15')
    button2 = telebot.types.InlineKeyboardButton("yes", callback_data='button17')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Would you like to add a third reward for your soulmate?", reply_markup=markup)
    
def ask_3reward(message):
    user_id = message.from_user.id
    user_3reward = message.text.strip().lower()
    
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_3reward = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_3reward,))
    conn.commit()
    conn.close()
    
    bot.send_message(user_id, "Awesome! How many lions should your soulmate spend to claim the third reward?")
    bot.register_next_step_handler(message, ask_3reward_cost)
    
def ask_3reward_cost(message):
    user_id = message.from_user.id
    reward_3cost = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  reward_3cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (reward_3cost,))
    conn.commit()
    conn.close()
    
    bot.send_message(user_id, "Thanks for sharing your information! Here's what I know about you:")
    send_user_data(message)

def send_user_data(message):
    user_id = message.from_user.id
    conn, cursor = get_user_db(user_id)
    cursor.execute("SELECT quser_name, soulmate_name, user_task, user_2task, user_3task, task_cost, task_2cost, task_3cost, user_reward, reward_cost, user_2reward, reward_2cost, user_3reward, reward_3cost, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        quser_name, soulmate_name, user_task, user_2task, user_3task, task_cost, task_2cost, task_3cost, user_reward, reward_cost, user_2reward, reward_2cost, user_3reward, reward_3cost, l_balance = user_data
        response =  f"💖{quser_name} and {soulmate_name}💖\nYour tasks are:\n1. {user_task} - for {task_cost} lions\n2. {user_2task} - for {task_2cost} lions\n3. {user_3task} - for {task_3cost} lions\nYour rewards are:\n1. {user_reward} - for {reward_cost} lions\n2. {user_2reward} - for {reward_2cost} lions\n3. {user_3reward} - for {reward_3cost} lions\nLions balance: {l_balance}"
    else:
        response = "I don't have your data yet. Please provide your information."
    bot.send_message(user_id, response)
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("yes", callback_data='button1')
    button2 = telebot.types.InlineKeyboardButton("no", callback_data='button2')
    markup.add(button1, button2)
    bot.send_message(user_id, "Want to edit?", reply_markup=markup)
    
def send_user_data(call):
    user_id = call.from_user.id
    conn, cursor = get_user_db(user_id)
    cursor.execute("SELECT quser_name, soulmate_name, user_task, user_2task, user_3task, task_cost, task_2cost, task_3cost, user_reward, reward_cost, user_2reward, reward_2cost, user_3reward, reward_3cost, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        quser_name, soulmate_name, user_task, user_2task, user_3task, task_cost, task_2cost, task_3cost, user_reward, reward_cost, user_2reward, reward_2cost, user_3reward, reward_3cost, l_balance = user_data
        response =  f"💖{quser_name} and {soulmate_name}💖\nYour tasks are:\n1. {user_task} - for {task_cost} lions\n2. {user_2task} - for {task_2cost} lions\n3. {user_3task} - for {task_3cost} lions\nYour reward are:\n1. {user_reward} - for {reward_cost} lions\n2. {user_2reward} - for {reward_2cost} lions\n3. {user_3reward} - for {reward_3cost} lions\nLions balance: {l_balance}"
    else:
        response = "I don't have your data yet. Please provide your information."
    bot.send_message(user_id, response)
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("yes", callback_data='button1')
    button2 = telebot.types.InlineKeyboardButton("no", callback_data='button2')
    markup.add(button1, button2)
    bot.send_message(user_id, "Want to edit?", reply_markup=markup)
    
def call2handler(call):
    user_id = call.from_user.id
    conn, cursor = get_user_db(user_id)
    cursor.execute("SELECT quser_name, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
    user_data = cursor.fetchone()
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
    bot.send_message(call.message.chat.id, f"Hello, {quser_name}!\n🦁: {l_balance}")#, reply_markup=markup)
    bot.send_photo(call.message.chat.id, file, reply_markup=markup)

# ----------------------------------------------- #
#                   callback                      #
#                                                 #
#                                                 #
#                                                 #
# ----------------------------------------------- #

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
            bot.send_message(call.message.chat.id, f"Hello, {quser_name}!\n🦁: {l_balance}")#, reply_markup=markup)
            bot.send_photo(call.message.chat.id, file, reply_markup=markup)    
    elif call.data == 'button5': #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        bot.send_message(user_id, "To get started, please tell me your name")
        bot.register_next_step_handler(call.message, edit_quser_name)
    elif call.data == 'button1': #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        bot.send_message(user_id, "To get started, please tell me your name")
        bot.register_next_step_handler(call.message, edit_quser_name)
    elif call.data == 'button3':
        bot.send_message(call.message.chat.id, "How much?") #plus
        bot.register_next_step_handler(call.message, pluslions)
    elif call.data == 'button4':
        bot.send_message(call.message.chat.id, "How much?") #minus
        bot.register_next_step_handler(call.message, minuslions)
    elif call.data == 'button6':
        markup = types.InlineKeyboardMarkup()
        return_button = types.InlineKeyboardButton("Return", callback_data='button7')
        markup.add(return_button)
        bot.send_message(call.message.chat.id, "you can:")
        bot.send_message(call.message.chat.id, "✨[say thank you](https://www.buymeacoffee.com/)✨", parse_mode="Markdown")
        bot.send_message(call.message.chat.id, "✨[contact me](https://t.me/levaau)✨", parse_mode="Markdown", reply_markup=markup)
    elif call.data == 'button7':
        call2handler(call)
    elif call.data == 'button8':
        call2handler(call)
    elif call.data == 'button9':
        markup = types.InlineKeyboardMarkup()
        return_button = types.InlineKeyboardButton("Return", callback_data='button7')
        markup.add(return_button)
        bot.send_message(call.message.chat.id, "✨[feel free to contact me](https://t.me/levaau)✨", parse_mode="Markdown", reply_markup=markup)
    elif call.data == 'button10': #same with 13
        bot.send_message(user_id, "Now, let's talk about the rewards. What's the first reward you'd like to offer in exchange for lions?")
        bot.register_next_step_handler(call.message, ask_reward)
    elif call.data == 'button11':
        bot.send_message(user_id, "Fantastic! What's the second task you'd like to create for your soulmate?")
        bot.register_next_step_handler(call.message, ask_user_2task)
    elif call.data == 'button12':
        bot.send_message(user_id, "Got it! What's the third task you'd like to create for your soulmate?")
        bot.register_next_step_handler(call.message, ask_user_3task)
    elif call.data == 'button14':
        bot.send_message(user_id, "Wonderful choice! What's the second reward you'd like to offer in exchange for lions?")
        bot.register_next_step_handler(call.message, ask_2reward)
    elif call.data == 'button15':
        bot.send_message(user_id, "Thanks for sharing your information! Here's what I know about you:")
        send_user_data(call)
    elif call.data == 'button17':
        bot.send_message(user_id, "Last but not least, what's the third reward you'd like to offer in exchange for lions?")
        bot.register_next_step_handler(call.message, ask_3reward)
    elif call.data == 'button18':
        bot.send_message(user_id, "Now, let's talk about the rewards. What's the first reward you'd like to offer in exchange for lions?")
        bot.register_next_step_handler(call.message, edit_reward)
    elif call.data == 'button19':
        bot.send_message(user_id, "Fantastic! What's the second task you'd like to create for your soulmate?")
        bot.register_next_step_handler(call.message, edit_user_2task)
    elif call.data == 'button20':
        bot.send_message(user_id, "Got it! What's the third task you'd like to create for your soulmate?")
        bot.register_next_step_handler(call.message, edit_user_3task)
    elif call.data == 'button13':
        bot.send_message(user_id, "Wonderful choice! What's the second reward you'd like to offer in exchange for lions?")
        bot.register_next_step_handler(call.message, ask_2reward)
    elif call.data == 'button16':
        bot.send_message(user_id, "Last but not least, what's the third reward you'd like to offer in exchange for lions?")
        bot.register_next_step_handler(call.message, edit_3reward)

    
    
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
            bot.send_message(user_id, f"Hello, {quser_name}!\n🦁: {l_balance}")#, reply_markup=markup)
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
            bot.send_message(user_id, f"Hello, {quser_name}!\n🦁: {l_balance}")#, reply_markup=markup)
            bot.send_photo(user_id, file, reply_markup=markup)
    else:
        bot.send_message(user_id, "Error: User data not found. Please make sure you have provided your information.")

# ----------------------------------------------- #
#                   editinfo                      #
#                                                 #
#                                                 #
#                                                 #
# ----------------------------------------------- #

@bot.message_handler(commands=['start_edit_info'])
def start_edit_info(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "To get started, please tell me your name")
    bot.register_next_step_handler(message, edit_quser_name)
def edit_quser_name(message):
    user_id = message.from_user.id
    quser_name = message.text.strip().lower()
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  quser_name = ? WHERE id = (SELECT MAX(id) FROM userdata)", (quser_name,))
    conn.commit()
    conn.close()
    bot.send_message(user_id, "Great! Now, I'd like to know your soulmate's name")
    bot.register_next_step_handler(message, edit_soulmate_name)
def edit_soulmate_name(message):
    user_id = message.from_user.id
    soulmate_name = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET soulmate_name = ? WHERE id = (SELECT MAX(id) FROM userdata)", (soulmate_name,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Thank you! What's the first task you'd like to create for your soulmate?")
    bot.register_next_step_handler(message, edit_user_task)
def edit_user_task(message):
    user_id = message.from_user.id
    user_task = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_task = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_task,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Wonderful! How many lions should your soulmate earn for completing the first task?")
    
    bot.register_next_step_handler(message, edit_task_cost)
def edit_task_cost(message):
    #cost
    user_id = message.from_user.id
    task_cost = message.text.strip().lower()
    #sql
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  task_cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (task_cost,))
    conn.commit()
    conn.close()
    # buttons
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("no", callback_data='button18')
    button2 = telebot.types.InlineKeyboardButton("yes", callback_data='button19')
    markup.add(button1, button2)
    bot.send_message(user_id, "Would you like to add a second task for your soulmate?", reply_markup=markup)
    
    #bot.register_next_step_handler(message, edit_reward)
    
def edit_user_2task(message):
    user_id = message.from_user.id
    user_2task = message.text.strip().lower()
    #sql
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_2task = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_2task,))
    conn.commit()
    conn.close()
    #cost
    bot.send_message(user_id, "Excellent choice! How many lions should your soulmate earn for completing the second task?")
    bot.register_next_step_handler(message, edit_2task_cost)
    
def edit_2task_cost(message):
    user_id = message.from_user.id
    task_2cost = message.text.strip().lower()
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  task_2cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (task_2cost,))
    conn.commit()
    conn.close()
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("no", callback_data='button18')
    button2 = telebot.types.InlineKeyboardButton("yes", callback_data='button20')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Would you like to add a third task for your soulmate?", reply_markup=markup)
    
def edit_user_3task(message):
    user_id = message.from_user.id
    user_3task = message.text.strip().lower()
    #sql
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_3task = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_3task,))
    conn.commit()
    conn.close()
    #cost
    bot.send_message(user_id, "Perfect! How many lions should your soulmate earn for completing the third task?")
    bot.register_next_step_handler(message, edit_3task_cost)
    
def edit_3task_cost(message):
    user_id = message.from_user.id
    task_3cost = message.text.strip().lower()
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  task_3cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (task_3cost,))
    conn.commit()
    conn.close()
    
    bot.send_message(user_id, "Now, let's talk about the rewards. What's the first reward you'd like to offer in exchange for lions?")
    bot.register_next_step_handler(message, edit_reward)
    
def edit_reward(message):
    user_id = message.from_user.id
    user_reward = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_reward = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_reward,))
    conn.commit()
    conn.close()

    bot.send_message(user_id, "Terrific! How many lions should your soulmate spend to claim the first reward?")
    bot.register_next_step_handler(message, edit_reward_cost)
    
    
def edit_reward_cost(message):
    user_id = message.from_user.id
    reward_cost = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  reward_cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (reward_cost,))
    conn.commit()
    conn.close()
    
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("no", callback_data='button15')
    button2 = telebot.types.InlineKeyboardButton("yes", callback_data='button13')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Would you like to add a second reward for your soulmate?", reply_markup=markup)
    
def edit_2reward(message):
    user_id = message.from_user.id
    user_2reward = message.text.strip().lower()
    
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_2reward = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_2reward,))
    conn.commit()
    conn.close()
    
    bot.send_message(user_id, "Great! How many lions should your soulmate spend to claim the second reward?")
    bot.register_next_step_handler(message, edit_2reward_cost)
    
def edit_2reward_cost(message):
    user_id = message.from_user.id
    reward_2cost = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  reward_2cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (reward_2cost,))
    conn.commit()
    conn.close()
    
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("no", callback_data='button15')
    button2 = telebot.types.InlineKeyboardButton("yes", callback_data='button16')
    markup.add(button1, button2)
    bot.send_message(message.chat.id, "Would you like to add a third reward for your soulmate?", reply_markup=markup)    
    
def edit_3reward(message):
    user_id = message.from_user.id
    user_3reward = message.text.strip().lower()
    
    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  user_3reward = ? WHERE id = (SELECT MAX(id) FROM userdata)", (user_3reward,))
    conn.commit()
    conn.close()
    
    bot.send_message(user_id, "Awesome! How many lions should your soulmate spend to claim the third reward?")
    bot.register_next_step_handler(message, edit_3reward_cost)
    
def edit_3reward_cost(message):
    user_id = message.from_user.id
    reward_3cost = message.text.strip().lower()

    conn, cursor = get_user_db(user_id)
    cursor.execute("UPDATE userdata SET  reward_3cost = ? WHERE id = (SELECT MAX(id) FROM userdata)", (reward_3cost,))
    conn.commit()
    conn.close()
    
    bot.send_message(user_id, "Thanks for sharing your information! Here's what I know about you:")
    send_user_data(message)    

@bot.message_handler(commands=['help'])
def help(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Hi there! Here's how Love & Lions works:\nYou create tasks and rewards for your soulmate, assign them a lion value, and then they complete tasks to earn lions. These lions can be spent to claim the rewards you've set up. It's all about showing appreciation!\nThe video tutorial can be found below 🤗")
    video = 'help.mp4'
    file = open('./' + video, 'rb')
    bot.send_video(message.chat.id, file)
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("yes", callback_data='button9')
    button2 = telebot.types.InlineKeyboardButton("no", callback_data='button8')
    markup.add(button1, button2)
    bot.send_message(user_id, "still confusing?", reply_markup=markup)

@bot.message_handler(commands=['profile'])
def profile(message):
    user_id = message.from_user.id
    conn, cursor = get_user_db(user_id)
    cursor.execute("SELECT quser_name, soulmate_name, user_task, user_2task, user_3task, task_cost, task_2cost, task_3cost, user_reward, reward_cost, user_2reward, reward_2cost, user_3reward, reward_3cost, l_balance FROM userdata WHERE id = (SELECT MAX(id) FROM userdata)")
    user_data = cursor.fetchone()
    conn.close()
    if user_data:
        quser_name, soulmate_name, user_task, user_2task, user_3task, task_cost, task_2cost, task_3cost, user_reward, reward_cost, user_2reward, reward_2cost, user_3reward, reward_3cost, l_balance = user_data
        response =  f"💖{quser_name} and {soulmate_name}💖\nYour tasks are:\n1. {user_task} - for {task_cost} lions\n2. {user_2task} - for {task_2cost} lions\n3. {user_3task} - for {task_3cost} lions\nYour reward are:\n1. {user_reward} - for {reward_cost} lions\n2. {user_2reward} - for {reward_2cost} lions\n3. {user_3reward} - for {reward_3cost} lions\nLions balance: {l_balance}"
    else:
        response = "I don't have your data yet. Please provide your information."
    photo = 'lions2.jpeg'
    file = open('./' + photo, 'rb')
    bot.send_photo(user_id, file)  
    bot.send_message(user_id, response)
    markup = telebot.types.InlineKeyboardMarkup()
    button1 = telebot.types.InlineKeyboardButton("yes", callback_data='button1')
    button2 = telebot.types.InlineKeyboardButton("no", callback_data='button2')
    markup.add(button1, button2)
    bot.send_message(user_id, "want to edit?", reply_markup=markup)
bot.polling(non_stop=True)