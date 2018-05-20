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
import urllib3
import ecartelera
import Movies.movies
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telepot.delegate import pave_event_space, per_chat_id, create_open, per_callback_query_origin
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent


TOKEN = '556801610:AAEDqKjjIZkWCJzARY_DwwIHzBoGjCImKZM'  # @Cicinebot
#TOKEN = '551454537:AAHZ_VFOqHqQO0lLMGtzJi0XsCYo5cCxvrM' # @cicinebotmaurizio
#TOKEN = '581607975:AAG995XceTIs5DjdW70blkjF3__IGCKv2_w'  # @CicinebotPablo_bot
#TOKEN = '574044701:AAHVro7hwe2YQ-VHXcXb5cVQJP1CYxyo5AE'  # @CicinebotMaria_bot
#TOKEN = '551454537:AAHZ_VFOqHqQO0lLMGtzJi0XsCYo5cCxvrM'  # @CicinebotMaurizio_bot
movieSelected = []


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
    data = []
    if 'infoPeli' in callback_key:
        data = list
    elif 'pelicula' in callback_key:
        for i in list:
            #print(i)
            data.append(ecartelera.getIdPelicula(i))
        #data = list
    elif 'cine' in callback_key:
        for i in list:
            #print(i)
            data.append(ecartelera.getIdCine(i))
    #print(data)
    else:
        data=list
    k = 0
    for n in list:
        button = InlineKeyboardButton(text=n, callback_data=callback_key + '/' + str(data[k]))
        buttones.append(button)
        print(button)
        k = k + 1
    return InlineKeyboardMarkup(inline_keyboard=build_menu(buttones, n_cols, header_buttons, footer_buttons))


#clase que gestiona los mensajes recibidos por el chat
class UserHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        #print (content_type, chat_type, chat_id)

        mensaje = msg['text']
        print("El usuario " + str(chat_id) + " escribió " + mensaje)

        if mensaje == '/start':

            optionList = ['Si', 'No']
            bot.sendMessage(chat_id, 'Buenas, soy CineBot, ¿te apetece ir al cine? 📽🎞🍿🥤🎬', reply_markup=build_buttons(optionList, 'start' , 2))

        elif mensaje == '/buscarCine':

            #aqui va la funcion que busca en la base de datos los cines
            cine = ecartelera.getCines()

            #envia lista de cines
            bot.sendMessage(chat_id, '¿A qué cine te apetece ir?', reply_markup=build_buttons(cine, 'cine', 1))

        elif '/buscarPelicula' in mensaje:

            # aqui va la funcion que busca en la base de datos peli[1] y return a lista de cine
            peli = mensaje.split('/buscarPelicula')
            found = True

            cineList = ['cine1', 'cine2', 'cine3', 'cine4']

            if found:
                bot.sendMessage(chat_id, 'Found it!')

                # envia lista de cine
                bot.sendMessage(chat_id, 'Donde quieres ir?', reply_markup=build_buttons(cineList, 'cine', 2))

            else:
                bot.sendMessage(chat_id, 'No he encontrado ninguna peli ' + peli[0])
                bot.sendPhoto(chat_id, ('ciaktriste.jpg', open('ciaktriste.jpg', 'rb')))


        elif mensaje == '/cineCercano':

            #recuperar la posicion del usuario
            #recuperar los cines mas cercano en la base de datos y ponerlos en una lista (cineList)

            cineList = ['cine1', 'cine2', 'cine3', 'cine4']
            bot.sendMessage(chat_id, 'Donde quieres ir?', reply_markup=build_buttons(cineList, 'cine', 2))


        elif mensaje == '/sugerirPelicula':

            bot.sendMessage(chat_id, '/sugerirPelicula: Todavia da hacer!')


        elif mensaje == '/help':

            bot.sendMessage(chat_id, 'Comandos:'
                                     '\n /buscarCine - Usa este comando para ver la cartelera del cine que quieras.'
                                     '\n /buscarPelicula - Usa este comando seguido del nombre de una pelicula para buscar los cines mas cercanos en los que se proyecta la pelicula.'
                                     '\n /cineCercano - Busca los cines mas cercanos basandose en tu ubicacion.'
                                     '\n /sugerirPelicula - Envia la informacion sobre una pelicula estrenada recientemente al azar.')

        else:

            bot.sendMessage(chat_id, 'Que quieres hacer?')
            bot.sendPhoto(chat_id, 'http://blog.pianetadonna.it/l67/wp-content/uploads/2014/10/punto_di_domanda.jpg')


#clase que gestiona los botones inchat
class ButtonHandler(telepot.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(ButtonHandler, self).__init__(*args, **kwargs)
    
    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        print ( "El usuario " + str(from_id) + " seleccionó " + query_data )

        if query_data == 'start/No':
            bot.sendMessage(from_id, '¡Qué pena! Espero verte pronto otra vez 🙂🙂🙂')
            bot.sendPhoto(from_id, ('ciaktriste.jpg', open('ciaktriste.jpg', 'rb')))


        elif query_data == 'start/Si':


            bot.sendPhoto(from_id, 'http://www.smeraldocinema.it/public/file/Cinemacard4.jpg')

            bot.sendMessage(from_id, '\nSi quieres puedes utilizar uno de estos comandos:'
                                     '\n /buscarCine - Usa este comando para ver la cartelera del cine elegido.'
                                     '\n /buscarPelicula - Usa este comando seguido del nombre de una pelicula para buscar los cines mas cercanos en los que se proyecta la pelicula.'
                                     '\n /cineCercano - Busca los cines mas cercanos basandose en tu ubicacion.'
                                     '\n /sugerirPelicula - Envia la informacion sobre una pelicula estrenada recientemente al azar.')

        elif 'infoPeli' in query_data:
    
            info = query_data.split('/')
            print ("Estas en elif infoPeli :" + str(info))

            infoRequest = info[6]


            movie = movieSelected[-1]
                # Movies.movies.Movie(movieSelected.movieName)
            
            #busca en la base de datos el atributo request de la peli
            
            if infoRequest == 'Director':
                bot.sendMessage(from_id, 'El director de la película es: ' + movie.director)
            
            elif infoRequest == 'Reparto':
                bot.sendMessage(from_id, 'Reparto: ' + movie.actors)
        
            elif infoRequest == 'Sinopsis':
                bot.sendMessage(from_id, 'Sinopsis: ' + movie.synopsis)
            
            elif infoRequest == 'Duracion':
                bot.sendMessage(from_id, 'La película dura ' + movie.duration + 'min')

            elif infoRequest == 'Valoraciones':
                stringValoration = ''
                val = int(movie.valoration[0:1])
                for i in range(0,val):
                    stringValoration += '⭐'
                bot.sendMessage(from_id, stringValoration)

            elif infoRequest == 'Generos':
                bot.sendMessage(from_id, movie.gender)



        elif 'pelicula' in query_data:

            mensaje = query_data.split('/')
            print("La pelicula es : " + str(mensaje))
            idPelicula = mensaje[3]

            nombreCine = ecartelera.getNombreCineById(mensaje[1])
            nombrePelicula = ecartelera.getNombrePeliculaById(idPelicula)
            bot.sendMessage(chat_id, 'Buscando la información de la película... Sea paciente')

            movie = Movies.movies.Movie(nombrePelicula)
            movieSelected.append(movie)
            bot.sendPhoto(from_id, movie.urlcartel)

            print (mensaje)
            idCine = ecartelera.getClaveCine(nombreCine)
            print ("El cine en el que se proyecta la película es: " + nombreCine + " y tiene el ID = " + idCine)
            pasesPelicula = ecartelera.getPasesDePelicula(idPelicula,idCine)
            #buscar pelicula

            infoPeli = ['Director', 'Reparto', 'Valoraciones', 'Sinopsis', 'Duracion', 'Generos']

            pases = ""
            for i in pasesPelicula:
                pases = pases + str(i) + " "
            
            data = mensaje[0] + '/' + mensaje[1] + '/' + mensaje[2] + '/' + idPelicula
            mensaje = "La pelicula " + nombrePelicula + " en el cine " + nombreCine  + ", tiene los siguientes pases: " + pases
            print(data)
            bot.sendMessage(from_id, mensaje , reply_markup=build_buttons(infoPeli, data + '/infoPeli/', 2))


        elif 'cine' in query_data:
    
            mensaje = query_data.split('/')
            idCine = mensaje[1]
            nombreCine = ecartelera.getNombreCineById(idCine)
            peli1List = ecartelera.getPeliculasEnCine(nombreCine)
            print ( peli1List)

            if len(peli1List) > 0:
                
                #envia cartelera
                string = "cine/" + str(idCine) + "/pelicula"
                #print (string)
                bot.sendMessage(from_id, "En el cine " + nombreCine + " están disponibles estas peliculas", reply_markup=build_buttons(peli1List, string, 1))
            
            else:
                bot.sendMessage(from_id, 'No he encontrado ningún cine ' + mensaje[1])
                bot.sendPhoto(from_id, ('ciaktriste.jpg', open('ciaktriste.jpg', 'rb')))


bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, UserHandler, timeout=3600
    ),

    pave_event_space()(
        per_callback_query_origin(), create_open, ButtonHandler, timeout=3600)
    ,
])


bot.message_loop(run_forever='Listening ...')
