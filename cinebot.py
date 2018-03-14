########################################################
#################### TELEGRAM BOT ######################
################ CINEBOT - @CICINEBOT ##################
## UCM - MÁSTER INGENIERÍA INFORMÁTICA - TMI - GRUPO 3 #
########################################################

##################### AUTORES ##########################
############## Andrés Aguirre Juárez ###################
############### Pablo Blanco Peris #####################
############# María Castañeda López ####################
############### Maurizio Vittorini #####################
########################################################


import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = '556801610:AAEDqKjjIZkWCJzARY_DwwIHzBoGjCImKZM'  # @Cicinebot


#función que gestiona los mensajes recibidos por el chat
def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    mensaje = msg['text']
    print(mensaje)

    if mensaje == '/start':
        bot.sendMessage(chat_id, 'Buenas, soy CineBot, ¿te apetece ir al cine?')
    else:
        bot.sendMessage(chat_id, mensaje)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
                       [InlineKeyboardButton(text='Tócame', callback_data='press')],
                   ])

        bot.sendMessage(chat_id, 'Prueba con el botón del chat', reply_markup=keyboard)


#función que gestiona los botones inchat
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    # print('Callback Query catch')
    # print('Callback Query:', query_id, from_id, query_data)

    bot.answerCallbackQuery(query_id, text='Te he pillado y lo sabes')


bot = telepot.Bot(TOKEN)

MessageLoop(bot, {'chat': on_chat_message,
                  # callback_query es el boton del chat
                  'callback_query': on_callback_query}).run_as_thread()
print('Listening ...')

while 1:
    time.sleep(10)

