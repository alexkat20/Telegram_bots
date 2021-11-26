"""
⎯ Какую вы хотите пиццу? Большую или маленькую?
⎯ Большую
⎯ Как вы будете платить?
⎯ Наличкой
⎯ Вы хотите большую пиццу, оплата - наличкой?
⎯ Да
⎯ Спасибо за заказ
"""

from transitions import Machine
import telebot


bot = telebot.TeleBot("1880855818:AAG8tq2RQOpWZ8VlwqlkfbyGNrMGmJOa9UY")


class Order_pizza(object):
    pass


# The states
states = ['q1', 'q2',
          'q3', 'q4']

transitions = [
    {'trigger': 'question1', 'source': 'q1', 'dest': 'q2'},
    {'trigger': 'question2', 'source': 'q2', 'dest': 'q3'},
    {'trigger': 'question3', 'source': 'q3', 'dest': 'q4'},
    {'trigger': 'question4', 'source': 'q4', 'dest': 'q1'}
]

order = Order_pizza()
# Initialize
machine = Machine(order, states=states, transitions=transitions, initial='q1')

user_answers = []


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Какую вы хотите пиццу? Большую или маленькую?")
    order.question1()


@bot.message_handler(content_types=['text'])
def get_text(message):
    if order.state == 'q2':
        if message.text.lower() != 'большую' and message.text.lower() != 'маленькую':
            bot.send_message(message.chat.id, "Извините, такого варианта нет. Выберите еще раз.")
        else:
            user_answers.append(message.text.lower())
            bot.send_message(message.chat.id, "Как вы будете платить?")
            order.question2()
    elif order.state == 'q3':
        user_answers.append(message.text.lower())
        bot.send_message(message.chat.id, f"Вы хотите {user_answers[0]} пиццу, оплата - {user_answers[1]}?")
        order.question3()
    elif order.state == 'q4':
        bot.send_message(message.chat.id, "Спасибо за заказ")
        order.question4()


bot.polling(none_stop=True)



