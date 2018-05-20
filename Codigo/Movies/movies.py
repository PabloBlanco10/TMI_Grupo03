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
    duration = None
    movieName = None
    valoration = None
    director = None
    gender = []
    actors = []
    synopsis = None
    urlcartel = None

    def __init__(self, movie):
        # Create the object that will be used to access the IMDb's database.
        self.ia = imdb.IMDb() # by default access the web.

        self.movieName = movie
        self.searchmovie()
        self.getinfofrommovie()
        self.getmovie()
        # self.data = []

    def searchmovie(self):
        # Search for a movie (get a list of Movie objects).
        self.result = self.ia.search_movie(self.movieName)


    def getinfofrommovie(self):
        # get first result
        for peli in self.result:
            # self.the_unt = self.result[0]
            self.the_unt = peli
            # self.ia.update(self.the_unt)
            self.ia.update(peli)
            tipo = self.the_unt['kind']
            ano = self.the_unt['year']
            if self.the_unt['kind'] is 'movie' and self.the_unt['year'] > 2017:
                return peli


    # Print some information.
    def getmovie(self):
        self.searchmovie()
        self.getinfofrommovie()
        translator = Translator()

        duracion = self.the_unt.get('runtime')
        valoracion = self.the_unt.get('rating')
        sinopsis = self.the_unt.get('plot outline')
        director = self.the_unt.get('director')
        duracion = self.the_unt.get('runtime')
        translation = translator.translate(sinopsis, dest='es')
        sinopsis = translation.text
        self.urlcartel = self.the_unt['cover url']

        generos = self.the_unt.get('genres')
        actores = self.the_unt.get('cast')
        actores = actores[0:10]

        stringActores = []
        for actor in actores:
            stringActores.append(actor['name'])

        stringGeneros = []
        for genero in generos:
            stringGeneros.append(genero)


        print("Película: " + self.movieName)

        print("Duracion: " + duracion[0])
        self.duration = duracion[0]

        print("Valoración: " + str(valoracion))
        self.valoration = str(valoracion)

        print("Director: " + director[0]['name'])
        self.director = director[0]['name']

       # print("Géneros: " + str(generos))
        self.gender = stringGeneros

        #print("Actores: " + stringActores)
        self.actors = stringActores

        print("Sinopsis: " + str(sinopsis))
        self.synopsis = str(sinopsis)
