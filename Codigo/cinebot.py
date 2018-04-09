########################################################
#################### TELEGRAM BOT ######################
################ CINEBOT - @CICINEBOT ##################
## UCM - MASTER INGENIERIA INFORMATICA - TMI - GRUPO 3 #
########################################################

##################### AUTORES ##########################
############## Andres Aguirre Juarez ###################
############### Pablo Blanco Peris #####################
############# Maria Castaneda Lopez ####################
############### Maurizio Vittorini #####################
########################################################


import sys
import time
import urllib2

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telepot.delegate import pave_event_space, per_chat_id, create_open, per_callback_query_origin
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent


#TOKEN = '556801610:AAEDqKjjIZkWCJzARY_DwwIHzBoGjCImKZM'  # @Cicinebot
TOKEN = '551454537:AAHZ_VFOqHqQO0lLMGtzJi0XsCYo5cCxvrM' # @cicinebotmaurizio




def on_notify_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    mensaje = msg['text']





#Use the following build_menu method to create a button layout with n_cols columns out of a list of buttons.

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):

    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def build_buttons(list, callback_key, n_cols, header_buttons=None, footer_buttons=None):

    buttones = []
    for n in list:
        buttones.append(InlineKeyboardButton(text=n, callback_data=callback_key + '/' + n))

    return InlineKeyboardMarkup(inline_keyboard=build_menu(buttones, n_cols, header_buttons, footer_buttons))





#funcion que gestiona los mensajes recibidos por el chat

class UserHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print (content_type, chat_type, chat_id)

        mensaje = msg['text']
        print(mensaje)

        if '/start' in mensaje:

            optionList = ['Yes', 'No']

            #keyboard = InlineKeyboardMarkup(inline_keyboard=[
            #    [InlineKeyboardButton(text='Yes', callback_data='StartSi')],
            #    [InlineKeyboardButton(text='No', callback_data='StartNo')],
            #])


            #bot.sendMessage(chat_id, 'Quieres ir al cine?', reply_markup=keyboard)

            bot.sendMessage(chat_id, 'Quieres ir al cine?', reply_markup=build_buttons(optionList, 'start' , 2))


            bot.sendAudio(chat_id=chat_id, audio=open('start.mp3', 'rb'))




        elif '/buscarCine' in mensaje:

            #aqui va la funcion que busca en la base de datos los cines

            cineList = ['cine1', 'cine2', 'cine3', 'cine4']

            #envia lista de cines
            bot.sendMessage(chat_id, 'Donde quieres ir?', reply_markup=build_buttons(cineList, 'cine', 2))



        elif '/buscarPelicula' in mensaje:

            peli = mensaje.split('/buscarPelicula')

            print peli

            # aqui va la funcion que busca en la base de datos peli[1] y return a lista de cine

            found = True

            cineList = ['cine1', 'cine2', 'cine3', 'cine4']

            if found:
                bot.sendMessage(chat_id, 'Found it!')

                # envia lista de cine
                bot.sendMessage(chat_id, 'Donde quieres ir?', reply_markup=build_buttons(cineList, 'cine', 2))


            else:
                bot.sendMessage(chat_id, 'No he encontrado algun peli ' + peli[0])
                bot.sendPhoto(chat_id, ('ciaktriste.jpg', open('ciaktriste.jpg', 'rb')))


        elif '/cineCercano' in mensaje:

            #recuperar la posicion del usuario
            #recuperar los cines mas cercano en la base de datos y ponerlos en una lista (cineList)

            cineList = ['cine1', 'cine2', 'cine3', 'cine4']

            bot.sendMessage(chat_id, 'Donde quieres ir?', reply_markup=build_buttons(cineList, 'cine', 2))


        elif '/sugerirPelicula' in mensaje:

            bot.sendMessage(chat_id, '/sugerirPelicula: Todavia da hacer!')


        elif '/help' or 'Help' in mensaje:


            #reply_markup = ReplyKeyboardRemove()
            #bot.sendMessage(chat_id=chat_id, text=None, reply_markup=reply_markup)

            bot.sendMessage(chat_id, 'Comandos:'
                                     '\n /buscarCine - Usa este comando para ver la cartelera del cine elegido.'
                                     '\n /buscarPelicula - Usa este comando seguido del nombre de una pelicula para buscar los cines mas cercanos en los que se proyecta la pelicula.'
                                     '\n /cineCercano - Busca los cines mas cercanos basandose en tu ubicacion.'
                                     '\n /sugerirPelicula - Envia la informacion sobre una pelicula estrenada recientemente al azar.')

        else:

            bot.sendMessage(chat_id, 'Que quieres hacer?')

            photo = urllib2.urlopen('https://thumbs.dreamstime.com/z/gente-bianca-3d-con-un-punto-interrogativo-27709668.jpg')
            bot.sendPhoto(chat_id, ('cine.jpg', photo))





#funcion que gestiona los botones inchat
class ButtonHandler(telepot.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(ButtonHandler, self).__init__(*args, **kwargs)

    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        # print('Callback Query catch')
        # print('Callback Query:', query_id, from_id, query_data)


        if query_data == 'start/No':
            bot.sendPhoto(from_id, ('ciaktriste.jpg', open('ciaktriste.jpg', 'rb')))


        elif query_data == 'start/Yes':

            bot.sendMessage(from_id, 'Que quieres hacer?')

            photo = urllib2.urlopen('http://www.smeraldocinema.it/public/file/Cinemacard4.jpg')
            bot.sendPhoto(from_id, ('cine.jpg', photo))

            bot.sendMessage(from_id, '\nComandos:'
                                     '\n /buscarCine - Usa este comando para ver la cartelera del cine elegido.'
                                     '\n /buscarPelicula - Usa este comando seguido del nombre de una pelicula para buscar los cines mas cercanos en los que se proyecta la pelicula.'
                                     '\n /cineCercano - Busca los cines mas cercanos basandose en tu ubicacion.'
                                     '\n /sugerirPelicula - Envia la informacion sobre una pelicula estrenada recientemente al azar.')

        elif 'cine' in query_data:

            cine = query_data.split('/')
            print cine

            #aqui va la funcion que busca en la base de datos el cine y return la cartelera del cine = lista de peliculas
            found = True

            peliList = ['peli1', 'peli2', 'peli3', 'peli4']

            if found:

                #envia cartelera
                bot.sendMessage(from_id, 'Que quieres ver?', reply_markup=build_buttons(peliList, 'pelicula', 2))

            else:
                bot.sendMessage(from_id, 'No he encontrado algun cine ' + cine[1])
                bot.sendPhoto(from_id, ('ciaktriste.jpg', open('ciaktriste.jpg', 'rb')))


        elif 'pelicula' in query_data:

            peli = query_data.split('/')
            print peli

            #buscar pelicula


            infoPeli = ['Sinopsis', 'Fotos', 'Reparto', 'Director', 'Valoraciones', 'Ultimas noticias', 'Trailer']

            bot.sendMessage(from_id, 'Que queires ver?', reply_markup=build_buttons(infoPeli, 'infoPeli/'+ peli[1] + '/', 2))


        elif 'infoPeli' in query_data:

            info = query_data.split('/')
            peli = info[1]
            infoRequest = info[2]

            #busca en la base de datos el atributo request de la peli

            bot.sendMessage(from_id, info)













#def on_inline_query(msg):
#
#    def compute():
#        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
#        print('Inline Query:', query_id, from_id, query_string)
#
#        mensaje = msg['text']
#        mensaje = query_string['text']
#
#
#        articles = [InlineQueryResultArticle(
#                        id='abc',
#                        title=query_string,
#                        input_message_content=InputTextMessageContent(
#                            message_text=query_string
#                        )
#                   )]
#
#        return articles
#
#    answerer.answer(msg, compute)
#
#
#
#def on_chosen_inline_result(msg):
#    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
#    print ('Chosen Inline Result:', result_id, from_id, query_string)






bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, UserHandler, timeout=3600 #Envia noticias
    ),

    pave_event_space()(
        per_callback_query_origin(), create_open, ButtonHandler, timeout=3600)
    ,
])




#answerer = telepot.helper.Answerer(bot)



bot.message_loop(run_forever='Listening ...')

