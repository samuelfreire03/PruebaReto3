﻿"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from prettytable import PrettyTable
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
def print5Avistamientos(avistamientos):
    """
    Imprime la información del autor seleccionado
    """
    if avistamientos == '':
        print('No se encontraron artistas nacidos en el rango dado')
    elif avistamientos:
        print("\n")
        print('5 primeras obras cargadas')
        primeros5 = lt.subList(avistamientos,1,5)
        x = PrettyTable(["Fecha", "Ciudad", 'Estado','Pais','Forma','Duracion (Segundos)','Duracion (Horas)','Comentarios','Fecha (Posteo)','Latitud','Longitud'])
        x._max_width = {"Fecha" : 10, "Ciudad" : 10,"Estado" : 10, "Pais" : 10,"Forma" : 10,"Duracion (Segundos)" : 10,"Duracion (Horas)" : 10,"Comentarios" : 10,"Fecha (Posteo)" : 10,"Latitud" : 10,"Longitud" : 10}
        for primeros in lt.iterator(primeros5):
            x.add_row([primeros['datetime'], primeros['city'], primeros['state'],primeros['country'],primeros['shape'],primeros['duration (seconds)'],primeros['duration (hours/min)'],primeros['comments']+'\n',primeros['date posted'],primeros['latitude'],primeros['longitude']])
        print(x)
        print("\n")
        print('5 primeras obras cargadas')
        ultimos5 = lt.subList(avistamientos,(int(lt.size(avistamientos))-4),5)
        y = PrettyTable(["Fecha", "Ciudad", 'Estado','Pais','Forma','Duracion (Segundos)','Duracion (Horas)','Comentarios','Fecha (Posteo)','Latitud','Longitud'])
        y._max_width = {"Fecha" : 10, "Ciudad" : 10,"Estado" : 10, "Pais" : 10,"Forma" : 10,"Duracion (Segundos)" : 10,"Duracion (Horas)" : 10,"Comentarios" : 10,"Fecha (Posteo)" : 10,"Latitud" : 10,"Longitud" : 10}
        for ultimos in lt.iterator(ultimos5):
            y.add_row([ultimos['datetime'], ultimos['city'], ultimos['state'],ultimos['country'],ultimos['shape'],ultimos['duration (seconds)'],ultimos['duration (hours/min)'],ultimos['comments']+'\n',ultimos['date posted'],ultimos['latitude'],ultimos['longitude']])
        print(y)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def print_avistamientos(author):
    """
    Imprime la información del autor seleccionado
    """
    if author:
        print("\n")
        x = PrettyTable(["Fecha", "Ciudad", 'Pais','Duracion (Segundos)','Forma'])
        x._max_width = {"Fecha" : 20, "Ciudad" : 20,"Pais" : 20, "Duracion (Segundos)" : 20,"Forma" : 20}
        for artistas in lt.iterator(author):
            x.add_row([artistas['datetime']+'\n', artistas['city'],artistas['country'],artistas['duration (seconds)'],artistas['shape']])
        print(x)
        print("\n")
    else:
        print('No se encontro el autor.\n')

def printMenu():
    print("Bienvenido")
    print("1- Crear el catalogo")
    print("2- Cargar información en el catálogo")
    print("3- Avistamientos por ciudad y rango de duracion")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Inicializando....\n")
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("Cargando información de los archivos ....")
        controller.loadData(cont)
        print('Avistamientos cargados: ' + str(lt.size(cont['avistamientos'])))
        print5Avistamientos(cont['avistamientos'])

    elif int(inputs[0]) == 3:
        llavevalor = om.get(cont['IndiceCiudad'],'phoenix')
        valor = me.getValue(llavevalor)['FechaIndice']
        valores = om.valueSet(valor)
        lista3primeros = lt.subList(valores,1,3)
        primeros3avistamientos = lt.newList('ARRAY_LIST')
        for c in lt.iterator(lista3primeros):
            for j in lt.iterator(c['ListaAvistamientosporFecha']):
                if int(lt.size(primeros3avistamientos)) < 3:
                    lt.addLast(primeros3avistamientos,j)
        print_avistamientos(primeros3avistamientos)

        lista3ultimos = lt.subList(valores,int(lt.size(valores))-2,3)
        ultimos3avistamientos = lt.newList('ARRAY_LIST')
        for c in lt.iterator(lista3ultimos):
            for j in lt.iterator(c['ListaAvistamientosporFecha']):
                lt.addLast(ultimos3avistamientos,j)
        lista_final = lt.subList(ultimos3avistamientos,int(lt.size(ultimos3avistamientos))-2,3)
        print_avistamientos(lista_final)

    else:
        sys.exit(0)
sys.exit(0)
