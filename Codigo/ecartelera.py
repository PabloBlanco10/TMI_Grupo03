# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import urllib
from bs4 import BeautifulSoup
import urllib.request
import requests
import MySQLdb

def conecction():
    conn = MySQLdb.connect(host= "localhost",
                           user="root",
                           passwd="",
                           db="cinebot")
                           
    return conn

def cargarCinesEnBBDD(nombreCine, enlaceCine):
    i = 0
    conn = conecction()
    x = conn.cursor()

    for cine in nombreCine:

        query = "INSERT IGNORE INTO Cine (nombre, enlace) VALUES ('{0}', '{1}');" .format(cine, enlaceCine[i])
        
        try:
            print(query)
            x.execute(query)
        except MySQLdb.ProgrammingError:
            print("La siguiente query ha fallado:%s" % query + '\n')
        print("El cine " + str(cine) + " ha sido añadido con el enlace " + enlaceCine[i])
        i = i + 1
    
    conn.commit()
    x.close()
    conn.close()

def cargarPasesEnBBDD(enlaceCine, pelicula, hora):
    i = 0
    conn = conecction()
    x = conn.cursor()
    
    query = "INSERT IGNORE INTO Pases (nombreCine, nombrePelicula, hora) VALUES ('{0}', '{1}', '{2}');" .format(enlaceCine, pelicula, hora)
        
    try:
        print(query)
        x.execute(query)
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado:%s" % query + '\n')
    print("El cine " + str(enlaceCine) + " ha añadido la peli " + pelicula + " a la hora: " + hora)

    conn.commit()
    x.close()
    conn.close()

def leerCinesFichero(nombreFichero):
    nombreCine = list()
    enlaceCine = list()
    f = open(nombreFichero)
    linea = f.readline()
    while linea != "":
        l = linea.split("_")
        #print ("ENLACE: " + l[0] + " NOMBRE : " + l[1])
        nombreCine.append(l[1][:-1])
        enlaceCine.append(l[0])
        linea = f.readline()
    f.close()
    return (nombreCine, enlaceCine)

def buscarPeliEnBD(peli):
    conn = conecction()
    x = conn.cursor()
    escaped = re.escape(peli)

    query = "SELECT nombre FROM Pelicula WHERE nombre = '{0}';".format(escaped)
    
    try:
        x.execute(query)
        
    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')
    
    peli = peli.format(peli)
    for line in x:
        #print (line)
        if peli == line[0]:
            conn.commit()
            x.close()
            conn.close()
            return True
        conn.commit()
        x.close()
        conn.close()
        return False

def cargarPeliculasEnBBDD(pelicula):
    conn = conecction()
    x = conn.cursor()
    
    for p in pelicula:
        if (buscarPeliEnBD(p)==False):
            p = str(MySQLdb.escape_string(p))
            query = "INSERT IGNORE INTO Pelicula (nombre) VALUES ('{0}');" .format(p)
            
            try:
                print(query)
                x.execute(query)
            except MySQLdb.ProgrammingError:
                print("La siguiente query ha fallado:%s" % query + '\n')
            print("La pelicula " + str(p) + " ha sido añadida.")
    
    conn.commit()
    x.close()
    conn.close()


def buscarPeliculaEnCine(url):
    pelicula = list()
    peliculaPase =dict()
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'lxml')
    peliculas = soup.find_all('div', class_="lfilmb")
    soup = BeautifulSoup(str(peliculas), 'lxml')
    horarioPeliculas = soup.find_all('div', class_="cartelerascont")
    nombrePeliculas = soup.find_all('h4')
    cont = 0
    for i in nombrePeliculas:
        line = re.split("<|>",str(i))
        pelicula.append(line[6])
    #Esto solo debe hacerse una vez, sino fallará
    cargarPeliculasEnBBDD(pelicula)
    for i in horarioPeliculas:
        soup = BeautifulSoup(str(i), 'lxml')
        horas = soup.find_all('p', class_="stn")
        listaHorasPelicula = list()
        for h in horas:
            line = re.split("<|>",str(h))
            listaHorasPelicula.append(line[2])
        peliculaPase[pelicula[cont]] = listaHorasPelicula
        cont = cont + 1
    for i in peliculaPase:
        for time in peliculaPase[i]:
            print (str(i) + time)
            cargarPasesEnBBDD(url, i, time)
    return peliculaPase



#En fichero.txt están los enlaces a cada cine y el nombre de cada cines en una misma linea, separado por _
(nombreCine, enlaceCine) = leerCinesFichero("cinesMadrid.txt")

#Es necesario cargar los cines una vez en la BBDD
#cargarCinesEnBBDD(nombreCine, enlaceCine)

#url = 'https://www.ecartelera.com/cines/dreams-cinema-palacio-hielo/'
for url in enlaceCine:
    buscarPeliculaEnCine(url)



