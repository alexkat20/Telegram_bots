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
states = ['Какую вы хотите пиццу? Большую или маленькую?', 'Как вы будете платить?',
          'Вы хотите 1 пиццу, оплата - 2?', 'Спасибо за заказ']

transitions = [
    {'trigger': 'question1', 'source': 'Какую вы хотите пиццу? Большую или маленькую?', 'dest': 'Как вы будете платить?'},
    {'trigger': 'question2', 'source': 'Как вы будете платить?', 'dest': 'Вы хотите 1 пиццу, оплата - 2?'},
    {'trigger': 'question3', 'source': 'Вы хотите 1 пиццу, оплата - 2?', 'dest': 'Спасибо за заказ'},
    {'trigger': 'question4', 'source': 'Спасибо за заказ', 'dest': 'Какую вы хотите пиццу? Большую или маленькую?'}
]


order = Order_pizza()
# Initialize
machine = Machine(order, states=states, transitions=transitions, initial='Какую вы хотите пиццу? Большую или маленькую?')

user_answers = []


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, order.state)
    order.question1()
    bot.register_next_step_handler(message, answer1)


def answer1(message):
    if message.text.lower() != 'большую' and message.text.lower() != 'маленькую':
        bot.send_message(message.chat.id, "Извините, такого варианта нет. Выберите еще раз.")
        #  order.question4()
        bot.register_next_step_handler(message, answer1)
    else:
        user_answers.append(message.text.lower())
        bot.send_message(message.chat.id, order.state)
        order.question2()
        bot.register_next_step_handler(message, answer2)


def answer2(message):
    user_answers.append(message.text)
    bot.send_message(message.chat.id, order.state.replace('1',
                                                          user_answers[0].lower()).replace('2', user_answers[1].lower()))
    order.question3()
    bot.register_next_step_handler(message, answer3)


def answer3(message):
    bot.send_message(message.chat.id, order.state)
    order.question4()
    #bot.register_next_step_handler(message, capital)


bot.polling(none_stop=True)



