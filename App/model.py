﻿"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf
import datetime

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def newCatalogo():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los crimenes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    catalog = {'avistamientos': None}

    catalog['avistamientos'] = lt.newList('SINGLE_LINKED', compareAvistamientos)
    catalog['IndiceCiudad'] = om.newMap(omaptype='BST',
                                      comparefunction=compareCiudad)

    return catalog

# Funciones para agregar informacion al catalogo

def addAvistamiento(catalog, avistamiento):
    """
    """
    lt.addLast(catalog['avistamientos'], avistamiento)
    updateIndiceCiudad(catalog['IndiceCiudad'], avistamiento)
    return catalog

def updateIndiceCiudad(map, avistamiento):
    """
    Se toma la fecha del crimen y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de crimenes
    y se actualiza el indice de tipos de crimenes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de crimenes
    """
    ciudad = avistamiento['city']
    entry = om.get(map, ciudad)
    if entry is None:
        datentry = newDataEntry(avistamiento)
        om.put(map, ciudad, datentry)
    else:
        datentry = me.getValue(entry)
    addFechaIndex(datentry, avistamiento)
    return map

def addFechaIndex(datentry, avistamiento):
    """
    Actualiza un indice de tipo de crimenes.  Este indice tiene una lista
    de crimenes y una tabla de hash cuya llave es el tipo de crimen y
    el valor es una lista con los crimenes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['ListaAvistamientos']
    lt.addLast(lst, avistamiento)
    offenseIndex = datentry['FechaIndice']
    fecha_avistamiento = avistamiento['datetime']
    fecha_avistamiento = datetime.datetime.strptime(fecha_avistamiento, '%Y-%m-%d %H:%M:%S')
    offentry = om.get(offenseIndex, fecha_avistamiento.date())
    if (offentry is None):
        entry = newOffenseEntry(fecha_avistamiento.date(), avistamiento)
        lt.addLast(entry['ListaAvistamientosporFecha'], avistamiento)
        om.put(offenseIndex, fecha_avistamiento.date(), entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['ListaAvistamientosporFecha'], avistamiento)
    return datentry

# Funciones para creacion de datos

def newDataEntry(crime):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'FechaIndice': None, 'ListaAvistamientos': None}
    entry['ListaAvistamientos'] = lt.newList('SINGLE_LINKED', compareCiudad)
    entry['FechaIndice'] = om.newMap(omaptype='BST',
                                      comparefunction=compareCiudad)
    return entry

def newOffenseEntry(offensegrp, crime):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'Fecha': None, 'ListaAvistamientosporFecha': None}
    ofentry['Fecha'] = offensegrp
    ofentry['ListaAvistamientosporFecha'] = lt.newList('SINGLELINKED', compareCiudad)
    return ofentry

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

def compareAvistamientos(id1, id2):
    """
    Compara dos avistamientos
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def compareCiudad(date1, date2):
    """
    Compara dos fechas
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1

def compareFechas(offense1, offense2):
    """
    Compara dos tipos de crimenes
    """
    offense = me.getKey(offense2)
    if (offense1 == offense):
        return 0
    elif (offense1 > offense):
        return 1
    else:
        return -1

# Funciones de ordenamiento
