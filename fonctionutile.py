#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  6 09:16:19 2024

@author: j.troussier
"""
import multiprocessing # fonction pour le multiprocessing, et non multithreading
from playsound import playsound


def stringtoliste(string):# fonction qui transforme un phrase en liste de mot
    mot = ''
    liste = []
    for i in string:
        if i != ' ':
            mot += i
        else :
            liste.append(mot)
            mot = ''
    if mot != ' ':
        liste.append(mot)
    return liste

def matricetoliste(matrice): # fonction qui transforme une matrice en liste 
    liste = []
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            liste.append(matrice[i][j])
    return liste

def mattostring(mat):#fonction qui transforme un liste de mot en string
    string = ""
    j = 0
    while j != len(mat) :
        if mat[j] != '' and j != len(mat) -1:
            string += mat[j] + " "
        elif mat[j] != '' and j == len(mat) -1:
            string += mat[j]
        j += 1
    return string

def soundtoplay(musique): #fonction qui permet de jouer de la musique 
    while(1):
        playsound(musique)

def jukebox(arg , p, *musique):# fonction qui lance la focntion soundtoplay sur un processeur autre que celui utiliser par le programme 
    if arg == 'start' :#si le premier argument de jukebox est 'start', il faut OBLIGATOIREMENT un troisième argument
        p = multiprocessing.Process(target=soundtoplay, args=(musique[0],))# fonction qui créer le process
        p.start()#on le lance
    else :# si un autre argument est utilisé, on arrète le process, et donc la musique...car la fonction playsound n'a aucun moyen de l'arréter tel quel...
        p.terminate()
    return p