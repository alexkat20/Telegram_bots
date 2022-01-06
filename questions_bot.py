import telebot
from datetime import datetime
import pandas as pd
import time
import schedule
from csv import writer
from threading import Thread


def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow(list_of_elem)


bot = telebot.TeleBot("1276052588:AAGXTwQ-URvk6uEo9oL4y1bexxN3XmI59Oc")


def send_message():
    today_date = datetime.now()
    birthdays = pd.read_csv('Birthdays.csv')
    for i in range(len(birthdays)):
        current_person = birthdays.loc[i]
        birthday = str(current_person[2]).split('.')
        #  print(birthday[0] == str(today_date.day) and birthday[1] == str(today_date.month), birthday[0],
        #      str(today_date.day), birthday[1], str(today_date.month))
        if birthday[0] == str(today_date.day) and birthday[1] == str(today_date.month):
            #  print(str(current_person[2]), '{}.{}'.format(str(today_date.day), str(today_date.month)))
            bot.send_message(485851611, "It's {}'s birthday today.".format(current_person[1]))


def do_schedule():
    schedule.every().day.at("10:00").do(send_message)
    schedule.every().day.at("17:00").do(send_message)
    schedule.every().day.at("13:00").do(send_message)
    while True:
        schedule.run_pending()
        time.sleep(1)


@bot.message_handler(commands=['add'])
def save_birthdays(message):
    command, name, date = message.text.split()
    bot.send_message(message.chat.id, "Added a new person and a birthday: {} {}".format(name, date))

    birthdays = pd.read_csv('Birthdays.csv')
    new_number = birthdays.loc(0)[len(birthdays) - 1][0] + 1

    row_contents = [new_number, name, date]

    append_list_as_row('Birthdays.csv', row_contents)

@bot.message_handler(commands=['help'])
def today_birthday(message):
    today_date = datetime.now()
    birthdays = pd.read_csv('Birthdays.csv')
    for i in range(len(birthdays)):
        current_person = birthdays.loc[i]
        birthday = str(current_person[2]).split('.')
        if birthday[0] == str(today_date.day) and birthday[1] == str(today_date.month):
            #  print(str(current_person[2]), '{}.{}'.format(str(today_date.day), str(today_date.month)))
            bot.send_message(485851611, "It's {}'s birthday today.".format(current_person[1]))
            break
    else:
        bot.send_message(485851611, "No birthdays today.")


@bot.message_handler(commands=['all'])
def all_birthdays(message):
    birthdays = pd.read_csv('Birthdays.csv')
    for i in range(len(birthdays)):
        bot.send_message(485851611, str(birthdays.loc[i][1]) + ' ' + str(birthdays.loc[i][2]))


def main_loop():
    thread = Thread(target=do_schedule)
    thread.start()
    bot.polling(none_stop=True, interval=5)


main_loop()
