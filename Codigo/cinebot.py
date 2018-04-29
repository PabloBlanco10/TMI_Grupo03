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

import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telepot.delegate import pave_event_space, per_chat_id, create_open, per_callback_query_origin
from telepot.namedtuple import InlineQueryResultArticle, InputTextMessageContent


TOKEN = '556801610:AAEDqKjjIZkWCJzARY_DwwIHzBoGjCImKZM'  # @Cicinebot
#TOKEN = '551454537:AAHZ_VFOqHqQO0lLMGtzJi0XsCYo5cCxvrM' # @cicinebotmaurizio


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
    if 'pelicula' in callback_key:
        #for i in list:
            #print(i)
            #data.append(ecartelera.getIdPelicula(i))
        data = list
    elif 'cine' in callback_key:
        for i in list:
            print(i)
            data.append(ecartelera.getIdCine(i))
    else:
        data = list
    print(data)
    k = 0
    for n in list:
        buttones.append(InlineKeyboardButton(text=n, callback_data=callback_key + '/' + str(data[k])))
        k = k + 1
    return InlineKeyboardMarkup(inline_keyboard=build_menu(buttones, n_cols, header_buttons, footer_buttons))


#clase que gestiona los mensajes recibidos por el chat
class UserHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        print (content_type, chat_type, chat_id)

        mensaje = msg['text']
        print(mensaje)

        if mensaje == '/start':

            optionList = ['Si', 'No']

            bot.sendMessage(chat_id, 'Buenas, soy CineBot, ¿te apetece ir al cine? 📽🎞🍿🥤🎬', reply_markup=build_buttons(optionList, 'start' , 2))
            #bot.sendAudio(chat_id=chat_id, audio=open('start.mp3', 'rb'))

        elif mensaje == '/buscarCine':

            #aqui va la funcion que busca en la base de datos los cines
            cine = ecartelera.getCines()

            #cineList = ['Yelmo Cines Plenilunio', 'Yelmo Cines Islazul', 'Cinesa Príncipe Pío 3D', 'La Vaguada']

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
                bot.sendMessage(chat_id, 'No he encontrado algun peli ' + peli[0])
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
        # print('Callback Query catch')
        # print('Callback Query:', query_id, from_id, query_data)
        print ( str(from_id) + " seleccionó " + query_data )

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
            print (info)
            peli = info[1]
            
            infoRequest = info[6]
            
            #busca en la base de datos el atributo request de la peli
            
            if infoRequest == 'Director':
                bot.sendMessage(from_id, 'Francis Lawrence')
            
            elif infoRequest == 'Reparto':
                bot.sendMessage(from_id, 'Jennifer Lawrence\n'
                                'Joel Edgerton\n'
                                'Matthias Schoenaerts\n'
                                'Egorov\n'
                                'Jeremy Irons\n'
                                'Joely Richardson\n')
        
            elif infoRequest == 'Sinopsis':
                bot.sendMessage(from_id, 'Francis Lawrence dirige esta película de suspense y espionaje basado en una '
                                'novela homónima escrita por Jason Matthews. Protagonizada por Jennifer Lawrence, '
                                'la historia se centra en Dominika Egorova, una joven rusa que pertenece al servicio '
                                'secreto de Rusia y ha sido entrenada por la Escuela Gorrión. Dicha escuela está especializada '
                                'en entrenar el cuerpo y la mente de las personas para que las utilicen como armas. Las iniciadas '
                                'aprenderán el arte de la seducción como método para conseguir sacar información de sus enemigos, '
                                'de una forma que no tengan que utilizar la violencia. Dominika sabe utilizar sus encantos y por ello, '
                                'se convierte en el miembro más peligroso de la Escuela Gorrión. Dominika tendrá su primer objetivo, '
                                'Nate Nash, un agente primerizo de la CIA, que vive en Rusia y es el encargado de los activos de la agencia.'
                                ' Los problemas llegarán para ella cuando descubra que hay un topo en su propia organización. Prepárate para '
                                'una misión donde el engaño, el misterio y el sexo serán los principales ingredientes.')
            
            elif infoRequest == 'Valoraciones':
                bot.sendMessage(from_id, '6.8: ⭐⭐⭐⭐⭐⭐⭐')



        elif 'pelicula' in query_data:

            peli = query_data.split('/')
            print("La pelicula es : " + str(peli))
            peliculaElegida = peli[3]
            cineElegido = ecartelera.getNombreCineById(peli[1])
            print ("EL ID DEL CINE ES: " + cineElegido)
            pasesPelicula = ecartelera.getPasesDePelicula(peli[3],peli[1])
            #buscar pelicula

            bot.sendPhoto(from_id, 'https://i.blogs.es/76dd90/gorrion-rojo/450_1000.jpg')

            infoPeli = ['Director', 'Reparto', 'Valoraciones', 'Sinopsis']

            pases = ""
            for i in pasesPelicula:
                pases = pases + str(i) + " "
            
            data = peli[1] + '/' + peli[2] + '/' + peli[3] + '/' + str(ecartelera.getIdPelicula(peliculaElegida))
            
            mensaje = "La pelicula " + peliculaElegida + " en el cine " + cineElegido # + ", tiene los siguientes pases: " + pases

            bot.sendMessage(from_id, mensaje , reply_markup=build_buttons(infoPeli, data + '/' + 'infoPeli/', 2))


        elif 'cine' in query_data:
    
            cine = query_data.split('/')
            idCine = cine[1]
            ultimoCine = ecartelera.getNombreCineById(idCine)
            #print (cine)
            peli1List = ['Cincuenta sombras liberadas', 'La forma del agua', 'Gorrión Rojo', 'Campeones']
            peli1List = ecartelera.getPeliculasEnCine(ultimoCine)

            idCine = ecartelera.getIdCine(ultimoCine)
            found = True

            if found:
                
                #envia cartelera
                string = "cine/" + str(idCine) + "/pelicula"
                print (string)
                bot.sendMessage(from_id, "En el cine " + ultimoCine + " están disponibles estas peliculas", reply_markup=build_buttons(peli1List, string, 1))
            
            else:
                bot.sendMessage(from_id, 'No he encontrado ningún cine ' + cine[1])
                bot.sendPhoto(from_id, ('ciaktriste.jpg', open('ciaktriste.jpg', 'rb')))
    


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
        per_chat_id(), create_open, UserHandler, timeout=3600
    ),

    pave_event_space()(
        per_callback_query_origin(), create_open, ButtonHandler, timeout=3600)
    ,
])

#answerer = telepot.helper.Answerer(bot)

bot.message_loop(run_forever='Listening ...')

