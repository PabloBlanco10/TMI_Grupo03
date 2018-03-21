########################################################
#################### TELEGRAM BOT ######################
################ CINEBOT - @CICINEBOT ##################
## UCM - MASTER INGENIERIA INFORMATICA - TMI - GRUPO 3 #
########################################################

##################### AUTORES ##########################
############## Andres Aguirre Juarez ###################
############### Pablo Blanco Peris #####################
############# Maria Castañeda Lopez ####################
############### Maurizio Vittorini #####################
########################################################


import sys
import time
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


TOKEN = '556801610:AAEDqKjjIZkWCJzARY_DwwIHzBoGjCImKZM'  # @Cicinebot
TOKEN = '581607975:AAG995XceTIs5DjdW70blkjF3__IGCKv2_w'  # @CicinebotPablo_bot
TOKEN = '574044701:AAHVro7hwe2YQ-VHXcXb5cVQJP1CYxyo5AE'  # @CicinebotMaria_bot
TOKEN = '551454537:AAHZ_VFOqHqQO0lLMGtzJi0XsCYo5cCxvrM'  # @CicinebotMaurizio_bot

#funcion que gestiona los mensajes recibidos por el chat
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


#funcion que gestiona los botones inchat
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

