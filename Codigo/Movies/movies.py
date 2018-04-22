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
import imdb
from googletrans import Translator



class Movie:

    def __init__(self):
        # Create the object that will be used to access the IMDb's database.
        self.ia = imdb.IMDb() # by default access the web.

        self.searchmovie()
        self.getinfofrommovie()
        self.getmovie()
        # self.data = []

    def searchmovie(self):
        # Search for a movie (get a list of Movie objects).
        movie = 'Black Panther'
        self.result = self.ia.search_movie(movie)


    def getinfofrommovie(self):
        # get first result
        self.the_unt = self.result[0]
        self.ia.update(self.the_unt)


    # Print some information.
    def getmovie(self):
        self.searchmovie()
        self.getinfofrommovie()
        translator = Translator()

        duracion = self.the_unt['runtime']
        valoracion = self.the_unt['rating']
        director = self.the_unt['director'] # get a list of Person objects.
        sinopsis = self.the_unt['plot outline']
        translation = translator.translate(sinopsis, dest='es')
        sinopsis = translation.text

        generos = self.the_unt['genres']
        urlcartel = self.the_unt['cover url']
        actores = self.the_unt['cast']
        actores = actores[0:10]
        stringActores = ''
        for actor in actores:
            stringActores += actor['name']+', '

        print("Duracion: " + duracion[0])
        print("Valoración: " + str(valoracion))
        print("Director: " + director[0]['name'])
        print("Géneros: " + str(generos))
        print("Actores: " + stringActores)
        print("Sinopsis: " + str(sinopsis))
