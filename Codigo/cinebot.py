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
from threading import Thread
import urllib3
import ecartelera
import math
import Movies.movies
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telepot.delegate import pave_event_space, per_chat_id, create_open, per_callback_query_origin
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent


#TOKEN = '556801610:AAEDqKjjIZkWCJzARY_DwwIHzBoGjCImKZM'  # @Cicinebot
#TOKEN = '551454537:AAHZ_VFOqHqQO0lLMGtzJi0XsCYo5cCxvrM' # @cicinebotmaurizio
#TOKEN = '581607975:AAG995XceTIs5DjdW70blkjF3__IGCKv2_w'  # @CicinebotPablo_bot
TOKEN = '574044701:AAHVro7hwe2YQ-VHXcXb5cVQJP1CYxyo5AE'  # @CicinebotMaria_bot
#TOKEN = '551454537:AAHZ_VFOqHqQO0lLMGtzJi0XsCYo5cCxvrM'  # @CicinebotMaurizio_bot
movieSelected = []
usersList = []



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

        if chat_id not in usersList:
            usersList.append(chat_id)

        if 'location' in msg.keys():
            localizacion = msg['location']
            print(localizacion)
            self.handle_location(localizacion, msg, chat_id)

        elif 'text' in msg.keys():
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
                peli = mensaje.split('/buscarPelicula ')

                if(peli[0] == '/buscarPelicula'):

                    bot.sendMessage(chat_id, 'Para utilizar el comando añade: /buscarPelicula seguido del nombre de la película')
                else:

                    cineList = ecartelera.buscarPelicula(peli[1])

                    if len(cineList) > 0:

                        peliculaActual = None
                        # envia lista de cine
                        for cine in cineList:
                            if(peliculaActual!= cine[1]):

                                peliculaActual = cine[1]

                                bot.sendMessage(chat_id, 'La pelicula' + cine[1] + ' que has buscado está en los siguientes cines: ')
                                time.sleep(1)
                            bot.sendMessage(chat_id, cine[0])
                            time.sleep(1)

                    else:
                        bot.sendMessage(chat_id, 'No he encontrado ninguna peli ' + peli[0])
                        bot.sendPhoto(chat_id, ('ciaktriste.jpg', open('ciaktriste.jpg', 'rb')))


            elif mensaje == '/cineCercano':

                #recuperar la posicion del usuario
                #recuperar los cines mas cercano en la base de datos y ponerlos en una lista (cineList)

                bot.sendMessage(chat_id, 'Por favor, envianos tu localización')


            elif mensaje == '/help':

                self.eviarComandos(chat_id)
            else:

                bot.sendMessage(chat_id, 'Que quieres hacer?')
                bot.sendPhoto(chat_id, 'http://blog.pianetadonna.it/l67/wp-content/uploads/2014/10/punto_di_domanda.jpg')

    def eviarComandos(self, chat_id):

        bot.sendMessage(chat_id, 'Comandos:'
                                 '\n /buscarCine - Usa este comando para ver la cartelera del cine que quieras.'
                                 '\n /buscarPelicula - Usa este comando seguido del nombre de una pelicula para buscar los cines en los que se proyecta la pelicula.'
                                 '\n /cineCercano - Busca los cines mas cercanos basandose en tu ubicacion.')

    def handle_location(self, localizacion, msg, chat_id):

        listaDatosCine = ecartelera.getCoordenadasCine()  # Lista de (Id y coordenadas) de todas los cines
        listacinesCercanos = []

        latitudMes = localizacion['latitude']
        longitudMes = localizacion['longitude']

        pi = 3.14
        radio = 6378.137
        grado = math.pi / 180
        latM = latitudMes * grado
        longM = longitudMes * grado

        for datosCine in listaDatosCine:
            latitud1 = datosCine[0]  # del cine que buscamos
            longitud1 = datosCine[1]  # del cine que buscamos
            lat1 = latitud1 * grado
            long1 = longitud1 * grado
            dlong = long1 - longM
            distancia = math.acos(
                math.sin(lat1) * math.sin(latM) + math.cos(lat1) * math.cos(latM) * math.cos(dlong)) * radio
            listacinesCercanos.append((distancia, datosCine[0], datosCine[1], datosCine[2]))

        listacinesCercanos.sort()

        for cine in listacinesCercanos[:3]:
            bot.sendLocation(chat_id, latitude=cine[1], longitude=cine[2]);
            time.sleep(3)

            # bot.sendMessage(chat_id, reply_markup=build_buttonsCineCercano(cine[3],'cercano', 1))
            print(cine)
        self.eviarComandos(chat_id)

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
                                     '\n /buscarPelicula - Usa este comando seguido del nombre de una pelicula para buscar los cines en los que se proyecta la pelicula.'
                                     '\n /cineCercano - Busca los cines mas cercanos basandose en tu ubicacion.')

        elif 'infoPeli' in query_data:
    
            info = query_data.split('/')
            print ("Estas en elif infoPeli :" + str(info))

            infoRequest = info[6]

            nombrePelicula = ecartelera.getNombrePeliculaById(info[3])
            #movie = Movies.movies.Movie(nombrePelicula)
            for movies in movieSelected:
                if movies.movieName == nombrePelicula:
                    movie = movies

                # Movies.movies.Movie(movieSelected.movieName)

            #busca en la base de datos el atributo request de la peli
            
            if infoRequest == 'Director':
                bot.sendMessage(from_id, 'El director de la película es: ' + movie.director)
            
            elif infoRequest == 'Reparto':
                actores = ', '.join(movie.actors)
                bot.sendMessage(from_id, 'Reparto: ' + actores)
        
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
                generos = ', '.join(movie.gender)
                bot.sendMessage(from_id, 'Generos: ' + generos)



        elif 'pelicula' in query_data:

            mensaje = query_data.split('/')
            print("La pelicula es : " + str(mensaje))
            idPelicula = mensaje[3]

            nombreCine = ecartelera.getNombreCineById(mensaje[1])
            nombrePelicula = ecartelera.getNombrePeliculaById(idPelicula)
            bot.sendMessage(from_id, 'Buscando la información de la película... Sea paciente')

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


# thread que verifica cada sleepTime segundos si hay nuevas películas en los cines
# y en caso envía una notifación a los usuarios
class ControlNotification(Thread):
    def __init__(self, peliList, sleepTime):
        Thread.__init__(self)
        self.peliList = peliList
        self.sleepTime = sleepTime

    # controla si hay nuevas peliculas en el DB
    def controlNews(self):

        newListPeli = ecartelera.getIdPeliculas()
        idNew = []
        nombreNew = []
        change = False

        if self.peliList != newListPeli:
            for id in newListPeli:
                if id not in self.peliList:
                    idNew.append(id)
                    change = True

        if change:
            for id in idNew:
                nombreNew.append(ecartelera.getNombrePeliculaById(id))
            return nombreNew

        else:
            return None


    # escribe las peliculas en una stringa de texto
    def parseList(self, peli):
        for p in peli:
            str = "-" + p + "\n"
        return str


    def run(self):
        while True:
            news = self.controlNews()

            if news is not None:
                for chat_id in usersList:
                    bot.sendMessage(chat_id, '💥¡NEWS!💥 \n¡Ha salido una nueva peli!📽🎞🍿🥤🎬\n ' + self.parseList(news))
            else:
                time.sleep(self.sleepTime)
                # print("No change, sleep\n")

            self.peliList = ecartelera.getIdPeliculas()
            ecartelera.cargarPeliculaEnBBDD("La graduación de los españoles")


controlThread = ControlNotification(ecartelera.getIdPeliculas(), 120)
controlThread.start()

bot.message_loop(run_forever='Listening ...')
