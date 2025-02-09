#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 08:06:40 2024

@author: j.troussier
"""

from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
import tkinter.ttk as t
from fonctionutile import *

'''
requirement : playsound en version 1.2.2, car la dernière version ne fonction pas
multiprocessing, donc un processeur a plusieur CORE
le programme a été tester sur visual studio et spyder WINDOWS il est fonctionnel bien que l'api winmmm a tendance a ne pas pouvoir lire le titre des musique...
le programme est une machine a gaz et le multiprocessing, la lecture de fichier intensive n'aide pas
il a été tester et reconnu que sur les machines des chartreux, spyder a du mal a terminer un process, ceci entrainant la continuation sans fin des musiques et par conséquence l'absence de changement de ses dernière...
pour arrêter les musique, méter fin a la fenêtre et terminé la console
j'ai essaye de rendre le programme le plus claire possible en annotant et en commantant mais je m'xcuse par avance si des bout sont inconpréhensible.
Je m'excuse d'ailleur pour toues les fautes d'orthographes du au manque de considération sur les descriptions
'''
world = 0
worldold = 0
position = [1,1]
oldposition = [1,1]
inventory = []
objetdisponible =[]
evenement = []
musique = ""
multiprocess = 0

def resizeImage(img, newWidth, newHeight): #fonction pour resize les image, elle ne vient pas de moi
    oldWidth = img.width()
    oldHeight = img.height()
    newPhotoImage = PhotoImage(width=newWidth, height=newHeight)
    for x in range(newWidth):
        for y in range(newHeight):
            xOld = int(x*oldWidth/newWidth)
            yOld = int(y*oldHeight/newHeight)
            rgb = '#%02x%02x%02x' % img.get(xOld, yOld)
            newPhotoImage.put(rgb, (x, y))
    return newPhotoImage
    
def confirmation(): #evenement commande confirmer
    global world, multiprocess, worldold, position, inventory, oldposition, objetdisponible,Tableau,evenement #la programmation tkinter nous pousse a l'utilisation de variable global 
    if world != worldold :
        worldold = world
        with open("monde/" + str(world)+"/intro.intro", encoding='utf-8') as intro: # boucle pour faire une transition entre les mondes
            retour.config(state="normal")
            for i in intro:
                retour.insert(END,i)
                retour.insert(END, "\n")
            retour.config(state="disabled") 
        musique = "musique/world" + str(world) + ".mp3"
        multiprocess = jukebox("stop", multiprocess)
        multiprocess = jukebox("start", multiprocess, musique)
    description = []
    description2 = []
    actionutilisateur = combo1.get() #on recupère la réponse du menu déroulant
    texteutilisateur = saisie.get() #on rerecupère la réponse dans le menu déroulant
    reponse = '' # variable de réponse du programme est ici
    print(actionutilisateur)
    print(texteutilisateur)
    if actionutilisateur == "autre" or actionutilisateur == '': # si l'utilisateur choisie l'option autre dans le menu déroulant, alors il n'y a uniquement le menu déroulant qui est pris en compte et on affiche quelque soit l'ooption le resutlat, l'entrée de l'utilisateur
        retour.config(state="normal")# cet état rend les ligne modifiable
        retour.insert(END,texteutilisateur+"\n")
        retour.config(state="disabled")#cet état rend les lignes non modifiable
        command = texteutilisateur
    else :
        retour.config(state="normal")
        retour.insert(END, actionutilisateur + " " + texteutilisateur+"\n")
        retour.config(state="disabled")
        command = actionutilisateur + " " + texteutilisateur
    retour.see("end")#cet commande ajuste la boite de dialogue a fin de voir les dernières modification
    command = stringtoliste(command.lower())
    print(command)
    indic = 0
    if command[0] == "aller": #si l'utilisateur commence par se déplacer
        if command[-1] == 'n' or command[-1] == 'nord':# on utilise les coordonnées d'une boussole
            position[0] +=1
        elif command[-1] == 's' or command[-1] == 'sud':
            position[0] -=1
        elif command[-1] == 'o' or command[-1] == 'ouest':
            position[1] -=1
        elif command[-1] == 'e' or command[-1] == 'est':
            position[1] +=1
        else:
            reponse = "deplacement non valide veuiller utiliser les coordonnées (n, nord...)" # comme se système n'est pas le plus efficace, si le joueur se trompe on lui montre un exemple de syntax correct 
        if oldposition != position: # si le joueur réussit a se déplacer, on teste si la pièce existe (si le fichier contenant la pièce existe)
            try : 
                with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r",encoding='utf-8') as worldtest:
                    for i in worldtest:
                        description.append(i)
                        description2.append(i)
                    if "conditionentre:\n" in description2: # ici on regarde si il y a des evenemnt necessaire pour rentrer dans la pièce
                         j = 0
                         while description[j] != "conditionentre:\n" :
                             j +=1
                         j+=1
                         while description[j] != "END\n": # on teste si le joueur si le joueur a débloquer tous les evenements nécessaires au débloquage d'une pièce
                             if description[j][:-1] not in evenement: # si ce n'est pas le cas, il est renvoyer en arrière 
                                 reponse = "vous ne pouvez pas passer comme sa..."
                                 position = oldposition[:]
                                 indic = 1
                             j +=1
                         if indic ==  0:
                           reponse = description[1]# si elle existe on affiche la description de la nouvelle pièce
                           oldposition = position[:]# et on modifie l'ancienne position 
                    else:
                        reponse = description[1]# si elle existe on affiche la description de la nouvelle pièce
                        oldposition = position[:]# et on modifie l'ancienne position
                    
            except :
                reponse = 'la pièce que vous tentez d\'accéder n\'existe malheureusement pas'#si la pèce n'existe pas, on retourne cette constatation
                position = oldposition[:]# et on récupère les anciennes positions
        image2 = PhotoImage(file="monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.png') #création d'image de background
        image2 = resizeImage(image2, 600,400)# on resize les image pour qu'elle puisse tenir dans le cadre
        Tableau.configure(image=image2) #changement d'image
        Tableau.image = image2
        retour.config(state="normal")
        retour.insert(END,reponse+"\n") # on affiche la reponse
        retour.config(state="disabled")
        retour.see("end")
        print(position)
    elif  command[0] == "inspecter":# si la commande d'observation est utiliser:
        if command[1] == 'inventaire':# l'on peut donner les objet que l'on a 
            reponse = "j'ai "
            retour.config(state="normal")
            retour.insert(END,reponse)
            if inventory != []:
                retour.insert(END, inventory)
            else:
                retour.insert(END, 'rien dans mon inventaire')
            retour.insert(END,"\n")
            retour.config(state="disabled")
        elif command[-1] in ['piece', 'pièce', 'salle', 'endroit']:#redonner la description de la pièce
            with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r", encoding='utf-8') as worldtest:
                    for i in worldtest:
                        description.append(i)
            reponse = description[1]
            retour.config(state="normal")
            retour.insert(END,reponse)
            retour.insert(END, "\n")
            retour.config(state="disabled")
        elif command[-1] in ['personne']:#donner les personnes interractible
            objet = []
            with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r", encoding='utf-8') as worldtest: #on recupère tout le fichier texte, ligne par ligne
                    for i in worldtest:
                        description.append(stringtoliste(i)) # on transforme chaque phrase en liste de mots
            i = 0
            try :
                while description[i][0] != "pnj:\n" : # on cherche la case comportant les dialogue...si elles existent
                    i +=1
                i+=1
                while description[i][0] != "END\n":# enssuite on recupère toutes les mots, d'indice 0 ce qui donne les noms des personnes
                    objet.append(description[i][0])
                    i +=1
                reponse = "il y a dans la pièce il y a :" + mattostring(objet) # enfin, on les affiche
            except:
                reponse = "il n'y a que moi ici" # enfin si personne n'est present dans la pièce... un message apparait
            retour.config(state="normal")
            retour.insert(END,reponse)
            retour.insert(END, "\n")
            retour.config(state="disabled")  
        elif command[-1] in ['objet', 'outil']:#donner les objets interractible
            objet = []
            with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r", encoding='utf-8') as worldtest:#on recupère tout le fichier texte, ligne par ligne
                    for i in worldtest:
                        description.append(stringtoliste(i))# on transforme chaque phrase en liste de mots
            i = 0
            try :
                while description[i][0] != "objet:\n" :# on cherche la case comportant les objets...si ils existent
                    i +=1
                i+=1
                while description[i][0] != "END\n":# enssuite on recupère toutes les mots, d'indice 0 ce qui donne les noms des personnes
                    print(description[i][0]) #debugging, non afficher dans la fenêtre, mais afficher dans la console pour vérifier que le programme a bien trouver
                    if description[i][0] not in inventory: # on affiche pas les objet qui ont déjà était pris par l'utilisateur
                        objet.append(description[i][0])# et on rajoute ce qui sont toujours présent dans la pièce
                    i +=1
                while description[i][0] != "eventobject:\n" :# on fait la même chose avec les objet qui demande une condition suplémentaire pour être utilisée( ex : porte fermé a clée...)
                    i +=1
                i+=1
                while description[i][0] != "END\n":
                    print(description[i][0])
                    if description[i][0] not in inventory: #condition redondante...
                        objet.append(description[i][0])
                    i +=1
                reponse = "il y a dans la pièce il y a :" + mattostring(objet)# enfin on les met dans la variable qui va afficher
            except:
                reponse = "il n'y a rien d'interessant ici" # si aucun objet n'est présent
            retour.config(state="normal")
            retour.insert(END,reponse)
            retour.insert(END, "\n")
            retour.config(state="disabled") 
        else: # description des objet en eux même...
            with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r", encoding='utf-8') as worldtest: #on rouvre le fichier ou le joueur est présent
                for i in worldtest:
                    description.append(stringtoliste(i)) # et on transforme chaque ligne en liste de mot...
            try :
                personne = '' # on initialise la variable donnant la description a '' soit vide
                i = 0
                while description[i][0] != "objet:\n" :# ensuite on se place dans la rubrique objet
                    i +=1
                while description[i][0] != "END\n":# ensuite jusqu'a la fin de cette rubrique, on cherche si un objet porte le nom de l'objet indiquer par l'utilisateur 
                    if description[i][0].lower() == command[-1]: # si c'est le cas, la DESCRIPTION (qui est une string) est rajouté a la varible de réponse 
                        personne = mattostring(description[i][:-2])
                    i +=1
                while description[i][0] != "eventobject:\n" : # on se place dès a present sur la rebrique des objets spéciaux
                    i +=1
                while description[i][0] != "END\n": # on regarde si l'objet mentionner par l'utilisateur existe dans la rubrique des objets spéciaux
                    if description[i][0].lower() == command[-1]:# si c'est le cas,
                        personne = []
                        j = 0
                        print("found")# indice débugage
                        while description[i][j] != "description:" :# on cherche l'indicateur de description
                            print(description[i][j])# indice débugage
                            j +=1
                        j+= 1
                        print("found2")# indice débugage
                        while description[i][j] != ":": #et on recopie mot par mot la description de l'objet, jusqu'à l'indicateur de fin soit ":"
                            personne.append(description[i][j])
                            j +=1
                        personne = mattostring(personne)
                        print("found3")# indice débugage
                    i +=1
                if personne == '':# si aucun objet ne correspond alors ce dernier est notifier...
                    reponse = "je ne suis pas sur que cette objet existe..."   
                else :
                    reponse = personne
            except: # si un erreur, pas d'event, pas d'objet, la réponse suivante est retourné
                reponse = "je ne comprends pas"
            retour.config(state="normal")
            retour.insert(END,reponse)
            retour.insert(END, "\n")
            retour.config(state="disabled") 
    elif command[0] in ['parler', 'discuter']:# commande des dialogues..., fonctionne exactement comme les description d'objet...
        with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r", encoding='utf-8') as worldtest:
            for i in worldtest:
                        description.append(stringtoliste(i))
        try :
            personne = ''
            i = 0
            while description[i][0] != "pnj:\n" :
                i +=1
            while description[i][0] != "END\n":
                if description[i][0].lower() == command[-1]:
                    personne = mattostring(description[i])
                i +=1
            if personne == '':
                reponse = "je ne suis pas sur que cette personne existe..."   
            else :
                reponse = personne 
        except:
            reponse = "je ne suis pas sur que parler avec vous-même puisse vous apporter quique ce soit d'interessant"
        retour.config(state="normal")
        retour.insert(END,reponse+"\n")
        retour.config(state="disabled")
    elif command[0] in ['prendre']: # commande pour récupere des objets
        objet=[]
        with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r", encoding='utf-8') as worldtest: # on recupère toutes le fichier texte 
                for i in worldtest:
                    objet.append(stringtoliste(i)) #on transforme toutes les lignes sous formes de liste de mot
        try :
            j = 0
            while objet[j][0] != "objet:\n" : # on se place dans la rebrique objet...
                j +=1
            j+=1
            reponse = "l'objet n'existe que dans votre imagination" # la réponse est initiliser avec la phrase d'echec
            while objet[j][0] != "END\n":# jusqu'à la fin de la rebrique, on cherche l'objet entré par l'utilisateur
                if objet[j][0] == command[-1]:
                    print(objet[j])# indice de debugage
                    if "2\n" in objet[j]:# si l'indice de l'objet est 2 ou non récuperable, la phrase suivante apparrait et l'objet N'est PAS récupérer
                        reponse="vous n'avez la volonté ou la force de le prendre" # nouvelle phrase pour la réponse, signifiant que l'objet n'as pas été récupérer mais existe...
                    elif objet[j][0] in inventory: # si l'objet a déjà été récupérer, il n'est pas récupérer a nouveau...
                        reponse = "vous posséder déjà cet objet"
                    else:
                        inventory.append(objet[j][0])# si l'objet existe, peut être récupérer, et n'a pas déjà été pris, on récupère l'objet ET la description associé et on le place dans la rebrique inventaire (une liste)
                        reponse ="vous avez pris "+ command[-1]
                j +=1
        except: # si l'objet n'existe pas ou une erreur est apparu...
            reponse = "l'objet n'existe que dans votre imagination"
        retour.config(state="normal")
        retour.insert(END,reponse)
        retour.insert(END, "\n")
        retour.config(state="disabled")
    elif command[0] in ['utiliser']:# commande utiliser...a noter qu'il faut deux argument, 1: l'objet a utiliser(provient de l'inventaire), 2: l'objet sur lequel l'utiliser(eventobjet) 
        event = []
        with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r", encoding='utf-8') as worldtest: # onrecupère le fichier et on transforme chacune des lignes en liste de mots
                for i in worldtest:
                    event.append(stringtoliste(i))
        if command[1] in inventory : # on verifie que l'objet que l'on cherche a utiliser est présent dans l'inventaire
            j = 0
            while event[j][0] != "eventobject:\n" : #on se place dans la rubrique des objets événement
                j +=1
            while event[j][0] != "END\n" and event[j][0] != command[-1]: # on vérifie que l'objet interractible existe... et on se place sur la ligne de l'evenement
                j += 1
                print(command[-1])# indice de debugage
                print(event[j][0])#indice de debugage
            if event[j][0] == command[-1] and event[j][4] not in evenement: # si l'événement existe, et qu'il n'a pas encore été effectué, c'est a dire que l'appelation de l'event n'est pas dans la liste evenement
                print(event[j])#indice de debugage
                if command[1] not in event[j]: #si l'objet que l'on cherche a utiliser N'est PAS present dans la ligne de l'evenement, cela signifie que ce n'était pas le bon objet a utilisé 
                    comteur = 0
                    while event[j][comteur] != "(nonefound)": # on se place au début de la case du retour si l'on a pas trouvée soit pour donner un indice au joueur de quelle objet utilisé 
                        comteur += 1
                    comteur += 2
                    while event[j][comteur] != ":":# et on copie cette description dans la réponse jusqu'a l'indicateur de fin de description
                        reponse += event[j][comteur] + " "
                        comteur += 1
                else: # en revanche si l'objet utilisé était le bon,
                    comteur = 0
                    while event[j][comteur] != "(iffound)": #on se place sur la rebrique de condition remplie
                        comteur += 1
                    comteur += 2
                    while comteur != len(event[j]): #on recopie jusqu'a la fin de la ligne la description de réussite
                        if event[j][comteur] != "upworld\n":# si l'instruction "upworld" n'est pas utilisé, on recopie simplement la description
                            reponse += event[j][comteur] + " "
                        else :# en revanche, si l'instruction upworld est présent, on change de monde, se qui se traduit par une réinitialisation de l'inventaire, des evenements et de la position ainsi qu'un changement de musique
                            retour.config(state="normal")
                            retour.insert(END,reponse)
                            retour.insert(END, "\n")
                            retour.config(state="disabled") 
                            world +=1
                            position = [1,1]
                            oldposition = [1,1]
                            inventory = []
                            evenement = []
                            description = []
                            with open("monde/" + str(world)+"/intro.intro", encoding='utf-8') as intro:
                                    retour.config(state="normal")
                                    for i in intro:
                                        retour.insert(END,i)
                                        retour.insert(END, "\n")
                                    retour.config(state="disabled") 
                            with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r", encoding='utf-8') as worldtest:
                                for i in worldtest:
                                    description.append(i)
                            image2 = PhotoImage(file="monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.png')
                            Tableau.configure(image=image2)
                            Tableau.image = image2
                            reponse = description[1]
                            retour.config(state="normal")
                            retour.insert(END,reponse+"\n") # on affiche la reponse
                            retour.config(state="disabled")
                            retour.see("end")
                            combo1.config(state="normal")
                            saisie.config(state="normal")
                            bouton.config(state="normal")
                            if world != worldold :# instruction de changement de musique
                                worldold = world
                                musique = "musique/world" + str(world) + ".mp3"
                                multiprocess = jukebox("stop", multiprocess)
                                multiprocess = jukebox("start", multiprocess, musique)
                        comteur += 1
                    if world == worldold :
                        evenement.append(event[j][4])
            elif event[j][4] in evenement : # si l'evenement a déjà été faite
                reponse = 'j\'ai déja fais cette action'
            else :# si l'instruction est erroné
                reponse = 'impossible d\'effectuer cette action'
        else : # sinon on refuse la comande
            reponse ="je ne suis pas sur de posséder cet objet"       
        retour.config(state="normal")
        retour.insert(END,reponse)
        retour.insert(END, "\n")
        retour.config(state="disabled")
    
    else:# si l'instruction ou la commande n'existe pas
        reponse = "je ne comprends pas"
        retour.config(state="normal")
        retour.insert(END,reponse+"\n")
        retour.config(state="disabled")
    if 'fin' in evenement : #si le jeu en vient sa fin, soit l'evenement 'fin' a été ajouté dans la liste des evenement du joueur 
        retour.config(state="normal")
        retour.insert(END,"bravo vous avez fini la démo\n")
        retour.config(state="disabled")
        bouton.config(state="disabled")
        combo1.config(state="disabled")
        saisie.config(state="disabled")
        retour.config(state="normal")
        retour.insert(END,"en espérant que tout ceci vous aura plus\n")
        retour.config(state="disabled")
    retour.see("end")  

def enterforconf(event): # fonction qui n'a pour but que de lancer la fonction du dessus mais avec la touche entrée au lieu d'appuyer sur le bouton confirmation
    confirmation()
    
    
def savecreator(): # menu déroulant pour sauvegarder son progrès
    save1 = filedialog.asksaveasfilename(title="sauvegarde", filetypes=[('save files','.save')]) + ".save" # création de la fenêtre
    save= open(save1, "w")# création de fichier tout a fait banal
    save.write("world : " + str(world) +" \n")
    save.write("position : " + str(position[0]) + " " + str(position[1])+" \n")
    save.write("inventory : ")
    for i in inventory :
        save.write(str(i) + " ")
    save.write("\n")
    save.write("evenement : ")
    for i in evenement :
        save.write(str(i) + " ")
    # a noter que les espaces sont IMPORTANT car sinon les mots prendrait un retour a la ligne...
    

def loadingsave(): # chargement des sauvegardes il faut recupérer mon algo de traitement des string dans le TIPE, fait
    global world,position, inventory,oldposition,evenement,multiprocess
    save = []
    description = []
    filename = filedialog.askopenfilename(title="chargement", filetypes=[('save files','.save')])# on demande a l'utilisateur de trouver l'emplacement de sont fichier de sauvegarde
    with open(filename, "r") as fichier: # récupère chaque information du fichier et on transforme les ligne en liste de mot
        for i in fichier :
            save.append(stringtoliste(i))
    print(save)# indice de debugage
    for i in range(len(save)):
        for j in range(len(save[i])):
            if save[i][j] == 'world':
                world = int(save[i][-2])
                worldold = [-1,-1]
                print(world)# indice de debugage
            if save[i][j] == 'position':
                position = [int(save[i][-3]),int(save[i][-2])]
                print(position)# indice de debugage
            if save[i][j] == 'inventory':
                inventory = save[i][2:-1]
                print(inventory)# indice de debugage
            if save[i][j] == 'evenement':
                evenement = save[i][2:-1]
                print(inventory)# indice de debugage
    with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r", encoding='utf-8') as worldtest: # on réaffiche la description dans laquelle le joueur est partie
        for i in worldtest:
            description.append(i)
    reponse = description[1]
    oldposition = position[:] # on récupere la position de sauvegarde
    image2 = PhotoImage(file="monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.png')# on réaffiche l'image de la salle dans laquelle le joueur est partie
    image2 = resizeImage(image2, 600,400)# on la reformatte pour quelle rentre dans le cadre
    Tableau.configure(image=image2) #on l'affiche
    Tableau.image = image2
    retour.config(state="normal")
    retour.insert(END,reponse+"\n") # on affiche la reponse
    retour.config(state="disabled")
    retour.see("end")
    combo1.config(state="normal")
    saisie.config(state="normal")
    bouton.config(state="normal")
    if world != worldold :# et on relance la musique du monde
        worldold = world
        musique = "musique/world" + str(world) + ".mp3"
        multiprocess = jukebox("stop", multiprocess)
        multiprocess = jukebox("start", multiprocess, musique)



def newgame():# on reinitialise TOUTES les valeurs, et on initialise les cases pour rentrer les informations
    global world,inventory,position,oldposition,evenement,multiprocess,worldold
    world = 1
    position = [1,1]
    oldposition = [1,1]
    inventory = []
    evenement = []
    description = []
    with open("monde/" + str(world)+"/intro.intro", encoding='utf-8') as intro: #on affiche l'intro du monde
            retour.config(state="normal")
            for i in intro:
                retour.insert(END,i)
                retour.insert(END, "\n")
            retour.config(state="disabled") 
    with open("monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.piece',"r", encoding='utf-8') as worldtest:
        for i in worldtest:
            description.append(i)
    image2 = PhotoImage(file="monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.png')
    Tableau.configure(image=image2)
    Tableau.image = image2
    reponse = description[1]
    retour.config(state="normal")
    retour.insert(END,reponse+"\n") # on affiche la reponse
    retour.config(state="disabled")
    retour.see("end")
    combo1.config(state="normal")
    saisie.config(state="normal")
    bouton.config(state="normal")
    if world != worldold : # on lance la musique de ce monde
        worldold = world
        musique = "musique/world" + str(world) + ".mp3"
        multiprocess = jukebox("stop", multiprocess)
        multiprocess = jukebox("start", multiprocess, musique)

def quit():# fonction qui termine la fenètre, le jeu ET la musique a cause du multiprocessing
    global multiprocess
    multiprocess = jukebox('stop', multiprocess)
    fenetre.quit()

    
if __name__ == "__main__":
    fenetre = Tk()# fenetre du jeu
    fenetre.geometry("800x600")# dimension de la fenètre
    fenetre.title('il était une démo')#titre de la fenetre
    #lancement de la musique d'attente
    musique = "musique/menu.mp3"
    multiprocess = jukebox("start", multiprocess , musique)
    #affichage de l'image de menu
    image1 = PhotoImage(file="monde/" + str(world) + "/" + str(position[0]) + ',' + str(position[1]) + '.png')
    image1 = resizeImage(image1, 600,400)
    #création d'un menu déroulant
    menubar = Menu(fenetre) 
    menu1 = Menu(menubar, tearoff=0)
    menu1.add_command(label="nouvelle partie", command=newgame)
    menu1.add_command(label="charger",command=loadingsave)
    menu1.add_command(label="sauvegarde",command = savecreator)
    menu1.add_separator()
    menu1.add_command(label="quitter",command=quit)
    menubar.add_cascade(label="Fichier", menu=menu1)
    #création d'une frame pour organiser rapidement une interface graphique
    frame1=LabelFrame(fenetre,text="commmande utilisateur")
    frame1.pack(side='bottom')
    #création d'une frame pour organiser rapidement le retour du programme
    frame2 = LabelFrame(fenetre, text ="retour programme", height = 10)
    frame2.pack(side='bottom')
    frame3 = LabelFrame(fenetre,text="rendu image")
    frame3.pack(side=TOP,fill="both", expand="yes")
    #retour du programme
    retour = scrolledtext.ScrolledText(frame2, wrap=WORD, width=80, height=8)
    retour.focus()
    retour.config(state="disabled")
    #menu déroulant
    combo1 = t.Combobox(frame1,values=["aller","prendre","parler","attaquer", "utiliser","inspecter","autre"])
    combo1.config(state="disabled")
    #bouton de confirmation qui renvoie a la fonction plus haut
    bouton =Button(frame1,text="confirmation", command=confirmation)
    bouton.config(state="disabled")

    #champ de saisie de texte
    saisie = Entry(frame1, width = 50)
    saisie.config(state="disabled")
    Tableau = Label(frame3,height=400,width=600)
    Tableau.configure(image=image1)
    fenetre.bind('<Return>', enterforconf)
    Tableau.pack(fill="both", expand="yes")
    retour.pack()
    bouton.pack(side='right')
    saisie.pack(side='right')
    combo1.pack(side='left')
    fenetre.config(menu=menubar)
    fenetre.mainloop()
    fenetre.destroy()