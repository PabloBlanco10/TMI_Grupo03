########################################################
#################### TELEGRAM BOT ######################
################ CINEBOT - @CICINEBOT ##################
## UCM - MÁSTER INGENIERÍA INFORMÁTICA - TMI - GRUPO 3 #
########################################################

##################### AUTORES ##########################
# Andrés Aguirre Juárez
# Pablo Blanco Peris
# María Castañeda López
# Maurizio Vittorini
########################################################


import sys
import time
import telepot
from telepot.loop import MessageLoop


TOKEN = '556801610:AAEDqKjjIZkWCJzARY_DwwIHzBoGjCImKZM'  # @Cicinebot


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # print(content_type, chat_type, chat_id)
    print(msg)

    if content_type == 'text':
        bot.sendMessage(chat_id, msg['text'])


bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(1)
