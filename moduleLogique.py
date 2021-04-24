"""
Module logique du jeu MagicMaze.
Auteurs : Théodore Garcher et Simon Eveillé

Contient les fonctions permettant la gestion des différents éléments du jeu.
"""
# IMPORTS ####################################################################

import random as rand
import upemtk as tk
from time import sleep, time
from varMM import *

# DEFINITION DES FONCTIONS ###################################################
def attributionDesTouches(nb_joueurs, touchesDeBase):
    """assigne aléatoire un nombre équitable de touches en fonction du nombre de joueurs"""
    nbTouchesNbJoueurs = {
        1: [7],
        2: [4, 3],
        3: [3, 2, 2]
    }

    nbTouchesJoueur = {
        1: 0,
        2: 0,
        3: 0
    }

    for i in range(1, nb_joueurs + 1):
        choix = rand.choice(nbTouchesNbJoueurs[nb_joueurs])
        nbTouchesJoueur[i] = choix
        nbTouchesNbJoueurs[nb_joueurs].remove(choix)

    touchesPartieParJoueur = dict()
    touchesPartie = dict()
    touchesDejaAttribuees = set()

    # Attribution des touches
    for numJoueur in range(1, nb_joueurs + 1):
        touchesPartieParJoueur[numJoueur] = {"changerPion": touchesDeBase[numJoueur]["changerPion"]}
        touchesPartieParJoueur[numJoueur] = {"elfe": touchesDeBase[numJoueur]["elfe"]}
        touchesDejaAttribuees.add("changerPion")
        touchesDejaAttribuees.add("elfe")
        for i in range(nbTouchesJoueur[numJoueur]):
            toucheAAttribuer = "changerPion"
            while toucheAAttribuer in touchesDejaAttribuees:
                toucheAAttribuer = rand.choice(list(touchesDeBase[numJoueur].keys()))
            touchesPartieParJoueur[numJoueur][toucheAAttribuer] = touchesDeBase[numJoueur][toucheAAttribuer]
            touchesPartie[toucheAAttribuer] = touchesDeBase[numJoueur][toucheAAttribuer], numJoueur
            touchesDejaAttribuees.add(toucheAAttribuer)
    return [touchesPartieParJoueur, touchesPartie]

def pause():
    """ Met pause, sort de ce mode lorsqu'on appuie sur ² renvoie le temps passé en pause"""
    heureDebut = time()
    
    tk.texte(875, 100, "PAUSE", couleur = "red", ancrage = "center", taille = 50)
    tk.mise_a_jour()
    
    entreeClavier = tk.attente_touche()
    while entreeClavier != "twosuperior":
        entreeClavier = tk.attente_touche()
    
    return time()-heureDebut

def debugMode():
    """
    Return une action aléatoire parmi les déplacements et le roulement de pion.
    Le mouvement a plus de chances d'arriver que le changement de pion
    Args:
        None
    Returns:
        Un caractère (str) parmi z, q, s, d, a
    """
    if rand.random() < 0.85:
        return rand.choice(['z', 'q', 's', 'd'])
    return 'a'


def initPions(numeroPion, position, infoPion):
    """
    Initialise le dictionnaire infoPion

    Args:
        numeroPion (TYPE): numero du pion à initialiser
        position (TYPE): position initiale du pion (ligne, colonne)
        infoPion (TYPE): dictionnaire contenant les informations de position des pions

    Returns:
        None.

    """
    # Dans le cas de l'initialisation, la position précédente et la position
    # actuelle sont les mêmes
    infoPion[numeroPion] = [position, position]
    return

def creerMatriceTerrain():
    """Initialise la matrice terrain à partier de la tuile de base, ainsi que les murs et les informations sur la position des tuiles"""
    matriceTerrain = [[None for colonne in range(50)] for ligne in range(50)]
    matriceTuiles = [['$' for colonne in range(50)] for ligne in range(50)]
    mursVer = [[0 for colonne in range(51)] for ligne in range(50)]
    mursHor = [[0 for colonne in range(50)] for ligne in range(51)]
    tuileDepart = tuile1()
    mursVerDepart = tuile1MursV()
    mursHorDepart = tuile1MursH()
    
    for ligne in range(len(tuileDepart)):
        for colonne in range(len(tuileDepart[0])):
            matriceTerrain[ligne+23][colonne+23] = tuileDepart[ligne][colonne]
            matriceTuiles[ligne+23][colonne+23] = '10'
    
    for ligne in range(len(mursVerDepart)):
        for colonne in range(len(mursVerDepart[0])):
            mursVer[ligne+23][colonne+22] = mursVerDepart[ligne][colonne]
    
    for ligne in range(len(mursHorDepart)):
        for colonne in range(len(mursHorDepart[0])):
            mursHor[ligne+22][colonne+23] = mursHorDepart[ligne][colonne]
            
    
    return matriceTerrain, matriceTuiles, mursVer, mursHor
    
    
            
def creerMurs():
    """Initialise les 2 matrices contenant respectivmeent les murs horizontaux et verticaux"""
    
    mursHor = [[0 for i in range(15)] for j in range(10-1)]
    mursVer = [[0 for i in range(15-1)] for j in range(10)]

    
    mursVer[6][6] = 1
    mursHor[6][6] = 1
    mursVer[3][7] = 1
    mursHor[3][7] = 1
    return mursHor, mursVer

def deplacementPion(numeroPion, direction, matriceTerrain, mursVer, mursHor, infoPion, sortieActive, listeGagnants, matriceTuiles):
    """
    Change la position du Pion dans le dictionnaire (en place) en le faisant
    avancer dans la direction voulue, si toutefois le déplacement est possible
    
    Args:
        direction (int): 0 = Nord ; 1 = Sud ; 2 = Est ; 3 = Ouest
        numeroPion (int): Entre 1 et 4
        matriceTerrain (list): matrice codant le terrain
        infoPion (dict): dictionnaire d'info sur la position des pions
        sortieActive (bool): Contient l'infomation de quelle sortie est active
        listeGagnants (list): Contient les numéros de pions ayant gagné

    Returns:
        None.
    """
    
    # Le tuple coordonneeDeplacment contient les modification à effectuer sur
    # la position d'un joueur, pour chaque direction 
    coordonneeDeplacement = ((-1, 0), (1, 0), (0, 1), (0, -1))
    
    # Déterminons la position visée
    ligneVisee = infoPion[numeroPion][0][0]+coordonneeDeplacement[direction][0]
    colonneVisee = infoPion[numeroPion][0][1]+coordonneeDeplacement[direction][1]
    
    # vérifions que la position visée est bien disponible
    # elle doit avoir une valeur != 0, être non-occupée, et existante sur le terrain
    # dans tous les cas si on ne peut pas se déplacer, la position précédente
    # devient la position actuelle
    
    # Existence de le case
    if ligneVisee < 0 or ligneVisee >= len(matriceTerrain):
        infoPion[numeroPion][1] = infoPion[numeroPion][0]
        return
    if colonneVisee < 0 or colonneVisee >= len(matriceTerrain[0]):
        infoPion[numeroPion][1] = infoPion[numeroPion][0]
        return
    
    # Liste des positions occupées 
    valeursDico = list(infoPion.values())
    positionOccupee = [ valeursDico[i][0] for i in range(len(valeursDico)) if i+1 not in listeGagnants]
    
    # Vérification que la case n'est pas occupée
    if (ligneVisee, colonneVisee) in positionOccupee:
        infoPion[numeroPion][1] = infoPion[numeroPion][0]
        return
    
    # Valeur différente de 0 ou None
    if matriceTerrain[ligneVisee][colonneVisee] == 0 or matriceTerrain[ligneVisee][colonneVisee] == None:
        infoPion[numeroPion][1] = infoPion[numeroPion][0]
        return
    
    # Vérification d'absence de mur
    if direction == 0 and mursHor[ligneVisee][colonneVisee]:
        infoPion[numeroPion][1] = infoPion[numeroPion][0]
        return
            
    elif direction == 1 and mursHor[infoPion[numeroPion][0][0]][infoPion[numeroPion][0][1]]:
        infoPion[numeroPion][1] = infoPion[numeroPion][0]
        return
        
    elif direction == 2 and mursVer[infoPion[numeroPion][0][0]][infoPion[numeroPion][0][1]]:
        infoPion[numeroPion][1] = infoPion[numeroPion][0]
        return
        
    elif direction == 3 and mursVer[ligneVisee][colonneVisee]:
        infoPion[numeroPion][1] = infoPion[numeroPion][0]
        return
        
    
    # Cas où les sorties sont actives et où le pion se déplace sur une sortie
    if sortieActive and matriceTerrain[ligneVisee][colonneVisee] == 'sortie':
        listeGagnants.append(numeroPion) # On ajoute le pion à la liste des gagnants
    
    # Gérer les gardes :
    # liste des tuiles utilisées par les pions
    listeTuilesPion = list()
    for pion in range(1, 5):
        if pion not in listeGagnants:
            ligne, colonne = infoPion[pion][0]
            listeTuilesPion.append(matriceTuiles[ligne][colonne][0])
    
    # liste des tuiles utilisées par les gardes
    listeTuilesGarde = list()
    for pion in infoPion.keys():
        if pion > 4:
            ligne, colonne = infoPion[pion][0]
            listeTuilesGarde.append(matriceTuiles[ligne][colonne][0])
            
    
    # Cas où un pion veut se déplacer sur la tuile d'un garde :
    if numeroPion in range(1, 5):
        if matriceTuiles[ligneVisee][colonneVisee][0] in listeTuilesGarde:
            infoPion[numeroPion][1] = infoPion[numeroPion][0]
            return
    
    # Cas où un garde veut se déplacer sur la tuile d'un pion :
    else:
        if matriceTuiles[ligneVisee][colonneVisee][0] in listeTuilesPion:
            infoPion[numeroPion][1] = infoPion[numeroPion][0]
            return
        
    # Si on arrive là, on peut procéder au déplacement
    infoPion[numeroPion] = [(ligneVisee, colonneVisee), infoPion[numeroPion][0]]
    return


def pionSurObjet(matriceTuiles, matriceTerrain, infoPion):
    """
    Vérifie si les pions sont sur leur objets respectifs

    Args:
        matriceTerrain (list): matrice qui encode le terrain
        infoPion (dict): dictionnaire des positions des joueurs
    Returns:
        True si tous les pions sont sur les bons objets
        False si ne serait-ce qu'un pion n'est pas sur son objet

    >>> infoPion = {1 : [(4, 7),(1, 1)], 2 : [(4, 8),(1, 1)], 3 : [(7, 7),(1, 1)], 4 : [(7,8),(1, 1)]}
    >>> pionSurObjet(matriceTerrain, infoPion)
    True
    >>> infoPion = {1 : [(4, 8),(1, 1)], 2 : [(4, 8),(1, 1)], 3 : [(7, 7),(1, 1)], 4 : [(7,8),(1, 1)]}
    >>> pionSurObjet(matriceTerrain, infoPion)
    False
    """
    # On initialise un compteur de conditions valides qui, si atteint, signifie que toutes les conditions sont réunies
    # pour activer la sortie
    nb_conditions_valides = 0
    # On vérifie pour chaque pion s'il se trouve sur la case de l'objet qui lui est associé
    # Si le bon pion est sur le bon objet, on incrémente le compteur
    for i in range(1, 5):
        if matriceTerrain[infoPion[i][0][0]][infoPion[i][0][1]] == 'o' + str(i):
            nb_conditions_valides += 1
    # Si le compteur atteint 4, toutes les conditions sont remplies, on renvoie True et on ajoute les 2 gardes supplémentaires
    if nb_conditions_valides == 4:
        ramassageObjets(matriceTerrain, infoPion)
        
        # Il faut trouver les coordonnées de la tuile 2 
        HG = None
        for ligne in range(len(matriceTuiles)):
            for colonne in range(len(matriceTuiles)):
                if matriceTuiles[ligne][colonne][0] != "$":
                    if int(matriceTuiles[ligne][colonne][0]) == 2:
                        HG = (ligne, colonne)
                        break
            if HG != None:
                break
        
        # Calcul des positions pour les 2 gardes
        direction = int(matriceTuiles[HG[0]][HG[1]][1])
        print(direction)
        garde2 = [[(0, 2), (3, 3), (3, 0), (0, 0)], [(0, 3), (2, 3), (3, 1), (1, 0)]]
        ligne1, ligne2 = HG[0]+garde2[0][direction][0], HG[0]+garde2[1][direction][0]
        colonne1, colonne2 = HG[1]+garde2[0][direction][1], HG[1]+garde2[1][direction][1]
        
        initPions(6, (ligne1,  colonne1), infoPion)
        initPions(7, (ligne2,  colonne2), infoPion)
        return True
    # Si une condition n'est pas remplie, on renvoie False
    return False


    sortieActive = True
    ramassageObjets(matriceTerrain, infoPion)

def pionSurSablier(matriceTerrain, infoPion):
    """return True si un pion est sur une case sablier et supprime la case du tableau"""
    # return False sinon
    for i in range(1, 5):
        if matriceTerrain[infoPion[i][0][0]][infoPion[i][0][1]] == 'sablier':
            matriceTerrain[infoPion[i][0][0]][infoPion[i][0][1]] = 1
            return True
    return False

def renverserHorizontalement(M):
    """Renverse une matrice selon un axe horizontal"""
    matrice = []
    for i in range(1, len(M) + 1):
        matrice.append(M[-i])
    M[:] = matrice

def transposer(M):
    """Transpose une matrice en place"""
    if len(M) == len(M[0]):
        n = len(M)
        for i in range(n-1):
            for j in range(i+1, n):
                stock = M[i][j]
                M[i][j] = M[j][i]
                M[j][i] = stock
    else:
        n = len(M)
        m = len(M[0])
        M2 = []

        for i in range(m):
            M2.append([0]*n)

        for i in range(n):
            for j in range(m):
                M2[j][i] = M[i][j]
        M[:] = M2

def rotationUnQuart(M):
    """Fait tourner de 90 un matrice dans le sens horaire"""
    renverserHorizontalement(M)
    transposer(M)

def detecterBord(coordonnees, matrice):
    """
    return la direction dans laquelle on explore
    """
    dico_positions = {(-1, 0): 0, #haut
                      (1, 0): 2, #bas
                      (0, -1): 3, #gauche
                      (0, 1): 1 #droite
    }
    for position, valeur in dico_positions.items():
        if matrice[coordonnees[0] + position[0]][coordonnees[1] + position[1]] == None:
            return valeur

def positionTuileExplo(coordonnees, direction):
    """
    return les coordonnées sur la matrice où il faut commencer à écrire la tuile explorée
    """
    if direction == 0:
        return coordonnees[0] - 4, coordonnees[1] - 1
    if direction == 1:
        return coordonnees[0] - 1, coordonnees[1] + 1
    if direction == 2:
        return coordonnees[0] + 1, coordonnees[1] - 2
    if direction == 3:
        return coordonnees[0] - 2, coordonnees[1] - 4
    
def extractionMatriceTuile(choix):
    """Renvoie la mini-matriceTerrain ainsi que les matrices de murs horizontaux et 
    Verticaux de la tuile selectionnée"""
    numero, direction = choix
    
    if numero == 2:
        matrice = tuile2()
        murV = tuile2MursV()
        murH = tuile2MursH()
    
    elif numero == 3:
        matrice = tuile3()
        murV = tuile3MursV()
        murH = tuile3MursH()
    
    elif numero == 4:
        matrice = tuile4()
        murV = tuile4MursV()
        murH = tuile4MursH()
    
    elif numero == 5:
        matrice = tuile5()
        murV = tuile5MursV()
        murH = tuile5MursH()
    
    elif numero == 6:
        matrice = tuile6()
        murV = tuile6MursV()
        murH = tuile6MursH()
    
    elif numero == 7:
        matrice = tuile7()
        murV = tuile7MursV()
        murH = tuile7MursH()
    
    elif numero == 8:
        matrice = tuile8()
        murV = tuile8MursV()
        murH = tuile8MursH()
    
    elif numero == 9:
        matrice = tuile9()
        murV = tuile9MursV()
        murH = tuile9MursH()
    
    # rotation de la tuile e fonction de la direction
    for i in range(direction):
        rotationUnQuart(matrice)
        rotationUnQuart(murV)
        rotationUnQuart(murH)
    
    # échange des murs horizontaux et verticaux en fonction de la direction
    if direction%2:
        murV, murH = murH, murV
    
    return matrice, murV, murH
    

def pionSurExploration(matriceTerrain, matriceTuiles, mursVer, mursHor, infoPion, tuilesRestantes, dicEsc, dic2, dic7, dicVortex, tuilesPosees, exploBool, telekinesieIndexTuileActive, modeTelekinesie, telekinesiesRestantes):
    """Vérifie si un pion est sur sa case d'exploration, si c'est le cas,
    place une nouvelle tuile au bon endroit"""
    
    # Vérification de si un pion est sur une case exploration correspondante à
    # une tuile non-explorée
    couplePionPos = list(infoPion.items())
    for pion, position in couplePionPos:
        if (len(tuilesRestantes)>0 and matriceTerrain[position[0][0]][position[0][1]] == 'exp'+str(pion)): #or (matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]] is str and matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]][:-1] == 'exp' and modeTelekinesie[0] == 1):
            # if (matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]] is str and matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]][:-1] == 'exp' and modeTelekinesie[0] == 1):
            #     pion = 3
            #     position = infoPion[3][0]
    
            direction = detecterBord(position[0], matriceTerrain)
            if direction == None:
                return
            
            exploAl = exploBool
            # sélection d'une tuile à ajouter au hasard si il n'y a pas de télékinésie
            if exploAl:
                choix = rand.choice(tuilesRestantes)
                tuilesRestantes.remove(choix)
                tuilesPosees.append(choix)
            else:
                telekinesie(matriceTerrain, matriceTuiles, tuilesPosees[telekinesieIndexTuileActive[0]], dicEsc, dicVortex, telekinesiesRestantes)
                choix = tuilesPosees[telekinesieIndexTuileActive[0]]
                telekinesieIndexTuileActive[0] = 0
            

            matrice, murV, murH = extractionMatriceTuile((choix, direction))
            
            # trouver la case à partir de laquelle ajouter la tuile sur plateau
            L, C = positionTuileExplo(position[0], direction)

            if choix == 2:
                for cle, valeur in dic2[direction].items():
                    dicEsc[(cle[0] + L, cle[1] + C)] = (valeur[0] + L, valeur[1] + C)
            if choix == 7:
                for cle, valeur in dic7[direction].items():
                    dicEsc[(cle[0] + L, cle[1] + C)] = (valeur[0] + L, valeur[1] + C)
            # changeons les valeurs de matriceTerrain et de matriceTuiles
            matriceTerrain[position[0][0]][position[0][1]] = 1
            
            for ligne in range(len(matrice)):
                for colonne in range(len(matrice[0])):
                    matriceTerrain[ligne+L][colonne+C] = matrice[ligne][colonne]
                    if matriceTerrain[ligne+L][colonne+C] in ('vortex1', 'vortex2', 'vortex3', 'vortex4'):
                        dicVortex[int(matriceTerrain[ligne+L][colonne+C][-1])].append((ligne+L, colonne+C))
                    matriceTuiles[ligne+L][colonne+C] = str(choix)+str(direction)
            for ligne in range(len(murV)):
                for colonne in range(len(murV[0])):
                    if mursVer[ligne + L][colonne + C - 1] == 0:
                        mursVer[ligne + L][colonne + C - 1] = murV[ligne][colonne]

            for ligne in range(len(murH)):
                for colonne in range(len(murH[0])):
                    if mursHor[ligne + L - 1][colonne + C] == 0:
                        mursHor[ligne + L - 1][colonne + C] = murH[ligne][colonne]
            
            # placement des gardes lors de l'apparition de la case 9
            garde9 = [(3,3), (0,3), (0,0), (3,0)]
            if choix == 9:
                initPions(5, (garde9[direction][0]+L, garde9[direction][1]+C), infoPion)
    
    # print(matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]], 'moulaga')
    # if type(matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]]) is str :
    #     print('censé être str',type(matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]]))
    #     print(matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]][:-1],'exp')
    #     print(modeTelekinesie, '1')
    if (type(matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]]) is str and matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]][:-1] == 'exp' and modeTelekinesie[0] == 1):
        position = infoPion[3][0]
        
        direction = detecterBord(position, matriceTerrain)
        if direction == None:
            return
        
        telekinesie(matriceTerrain, matriceTuiles, tuilesPosees[telekinesieIndexTuileActive[0]], dicEsc, dicVortex, telekinesiesRestantes)
        choix = tuilesPosees[telekinesieIndexTuileActive[0]]
        telekinesieIndexTuileActive[0] = 0
        matrice, murV, murH = extractionMatriceTuile((choix, direction))
        
        # trouver la case à partir de laquelle ajouter la tuile sur plateau
        L, C = positionTuileExplo(position, direction)

        if choix == 2:
            for cle, valeur in dic2[direction].items():
                dicEsc[(cle[0] + L, cle[1] + C)] = (valeur[0] + L, valeur[1] + C)
        if choix == 7:
            for cle, valeur in dic7[direction].items():
                dicEsc[(cle[0] + L, cle[1] + C)] = (valeur[0] + L, valeur[1] + C)
        # changeons les valeurs de matriceTerrain et de matriceTuiles
        matriceTerrain[position[0]][position[1]] = 1
        
        for ligne in range(len(matrice)):
            for colonne in range(len(matrice[0])):
                matriceTerrain[ligne+L][colonne+C] = matrice[ligne][colonne]
                if matriceTerrain[ligne+L][colonne+C] in ('vortex1', 'vortex2', 'vortex3', 'vortex4'):
                    dicVortex[int(matriceTerrain[ligne+L][colonne+C][-1])].append((ligne+L, colonne+C))
                matriceTuiles[ligne+L][colonne+C] = str(choix)+str(direction)
        for ligne in range(len(murV)):
            for colonne in range(len(murV[0])):
                if mursVer[ligne + L][colonne + C - 1] == 0:
                    mursVer[ligne + L][colonne + C - 1] = murV[ligne][colonne]

        for ligne in range(len(murH)):
            for colonne in range(len(murH[0])):
                if mursHor[ligne + L - 1][colonne + C] == 0:
                    mursHor[ligne + L - 1][colonne + C] = murH[ligne][colonne]
        
        # placement des gardes lors de l'apparition de la case 9
        garde9 = [(3,3), (0,3), (0,0), (3,0)]
        if choix == 9:
            initPions(5, (garde9[direction][0]+L, garde9[direction][1]+C), infoPion)
    return

def ramassageObjets(matriceTerrain, infoPion):
    """
    "Ramasse" les objets sur le terrain et remplace dans matrice terrain 'o1' à 'o4' par 1, qui correspond à une case normale.
    Args:
        matriceTerrain (list) : le terrain de jeu codé en format matriciel
        infoPion (dict) : dictionnaire des postions des pions
    Returns:
        None
    """
    
    # On parcourt les positions des joueurs et on remplace la valeur de la case
    # sur laquelle ils sont par 1
    listePions = infoPion.values()
    for positionObjet in listePions:
        ligne = positionObjet[0][0]
        colonne = positionObjet[0][1]
        matriceTerrain[ligne][colonne] = 1
    return

def selecteurPion(numPion, infoPion, listeGagnants):
    """
    Change le pion actuellement en train d'être joué par le suivant.
    Les pions suivent toujours le même roulement.
    Un pion qui a gagné (rentré dans la sortie) est sauté lors du roulement
    Args:
        numPion (int) : les entiers de 1 à 4 sont les valeurs possibles
        infoPion (dict) : dictionnaire contenant les clés correspondant à chaque pion (1 à 4)
        listeGagnants (list) : liste des pions ayant atteint la sortie
    Returns:
        numPion (int) + 1, sauf 4 qui devient 1
    >>> infoPion = {1: [(9, 0), (9, 1)], 2: [(4, 8), (5, 8)], 3: [(7, 7), (6, 7)], 4: [(7, 8), (6, 8)]}
    >>> listeGagnants = []
    >>> selecteurPion(1, infoPion, listeGagnants)
    2
    >>> selecteurPion(2, infoPion, listeGagnants)
    3
    >>> selecteurPion(3, infoPion, listeGagnants)
    4
    >>> selecteurPion(4, infoPion, listeGagnants)
    1
    >>> listeGagnants = [1, 2, 3]
    >>> selecteurPion(1, infoPion, listeGagnants)
    4
    """
    # On cherche le prochain pion jouable parmi la liste des pions valides (les pions non-gagnants)
    # while True:
    #     if ((numPion + 1) % 5 in infoPion) and ((numPion + 1) % 5 not in listeGagnants):
    #         return numPion + 1
    #     numPion = (numPion + 1) % 5
    numPion += 1
    while numPion in listeGagnants or numPion not in infoPion.keys():
        numPion = numPion+1 if numPion+1 < 8 else 1
    return numPion
        
def gestionEntreeClavier(matriceTerrain, mursVer, mursHor, infoPion, pionActif, sortieActive, debugActif, vitesse, listeGagnants, dicVortex, dicEsc, dicTuile2, dicTuile7, modeVortex, vortexActif, touchesPartie, touchesPartieParJoueur, nb_joueurs, touchesDeBase, tempsRestant, matriceTuiles, tuilesRestantes, tuilesPosees, telekinesieIndexTuileActive, modeTelekinesie, telekinesiesRestantes):
    """
    Regarde sur quelle touche le/les joueurs appuient, et réagit en conséquence

    Returns:
        None.

    """
    # Gestion du mode debug
    if debugActif == 1:
        entreeClavier = tk.attente_touche_jusqua(vitesse)
        if entreeClavier == None:
            entreeClavier = debugMode()
    
    # Mode normal 
    else:
        entreeClavier = tk.attente_touche_jusqua(250)

    # Gestion des entrées utilisateurs/debug
    if entreeClavier == touchesPartie['haut'][0]:
        deplacementPion(pionActif[touchesPartie['haut'][1]], 0, matriceTerrain, mursVer, mursHor, infoPion, sortieActive, listeGagnants, matriceTuiles)

    elif entreeClavier == touchesPartie['gauche'][0]:
        deplacementPion(pionActif[touchesPartie['gauche'][1]], 3, matriceTerrain, mursVer, mursHor, infoPion, sortieActive, listeGagnants, matriceTuiles)

    elif entreeClavier == touchesPartie['bas'][0]:
        deplacementPion(pionActif[touchesPartie['bas'][1]], 1, matriceTerrain, mursVer, mursHor, infoPion, sortieActive, listeGagnants, matriceTuiles)
    
    elif entreeClavier == touchesPartie['droite'][0]:
        deplacementPion(pionActif[touchesPartie['droite'][1]], 2, matriceTerrain, mursVer, mursHor, infoPion, sortieActive, listeGagnants, matriceTuiles)

    elif entreeClavier == touchesPartie['escalier'][0]:
        escalier(pionActif[touchesPartie['escalier'][1]], dicEsc, infoPion, listeGagnants)

    elif entreeClavier == touchesPartie['vortex'][0][0]:
        if pionActif[touchesPartie['vortex'][1]] < 5:
            activerVortex(pionActif[touchesPartie['vortex'][1]], dicVortex, infoPion, modeVortex, vortexActif, listeGagnants)

    elif entreeClavier == touchesPartie['vortex'][0][1] and modeVortex == [1]:
        selectVortex(vortexActif, dicVortex, pionActif[touchesPartie['vortex'][1]])

    elif entreeClavier == touchesDeBase[1]['changerPion']:
        pionActif[1] = selecteurPion(pionActif[1], infoPion, listeGagnants)

    elif entreeClavier == touchesDeBase[2]['changerPion'] and nb_joueurs in (2, 3):
        pionActif[2] = selecteurPion(pionActif[2], infoPion, listeGagnants)

    elif entreeClavier == touchesDeBase[3]['changerPion'] and nb_joueurs == 3:
        pionActif[3] = selecteurPion(pionActif[3], infoPion, listeGagnants)

    elif entreeClavier == touchesDeBase[1]['elfe'][0] and pionActif[1] == 3 and telekinesiesRestantes[0] > 0:
        activerModeTelekinesie(infoPion, telekinesieIndexTuileActive, tuilesPosees, modeTelekinesie, matriceTerrain, matriceTuiles, mursVer, mursHor, tuilesRestantes, dicEsc, dicTuile2, dicTuile7, dicVortex, telekinesiesRestantes)

    elif entreeClavier == touchesDeBase[2]['elfe'][0] and nb_joueurs in (2, 3) and pionActif[2] == 3 and telekinesiesRestantes[0] > 0:
        activerModeTelekinesie(infoPion, telekinesieIndexTuileActive, tuilesPosees, modeTelekinesie, matriceTerrain, matriceTuiles, mursVer, mursHor, tuilesRestantes, dicEsc, dicTuile2, dicTuile7, dicVortex, telekinesiesRestantes)

    elif entreeClavier == touchesDeBase[3]['elfe'][0] and nb_joueurs == 3 and pionActif[3] == 3 and telekinesiesRestantes[0] > 0:
        activerModeTelekinesie(infoPion, telekinesieIndexTuileActive, tuilesPosees, modeTelekinesie, matriceTerrain, matriceTuiles, mursVer, mursHor, tuilesRestantes, dicEsc, dicTuile2, dicTuile7, dicVortex, telekinesiesRestantes)

    elif entreeClavier == touchesDeBase[1]['elfe'][1] and modeTelekinesie == [1] and telekinesiesRestantes[0] > 0:
        selectTuileTelekinesie(telekinesieIndexTuileActive, tuilesPosees, matriceTuiles, infoPion, mursVer, mursHor, matriceTerrain)

    elif entreeClavier == touchesDeBase[2]['elfe'][1] and nb_joueurs in (2, 3) and modeTelekinesie == [1] and telekinesiesRestantes[0] > 0:
        selectTuileTelekinesie(telekinesieIndexTuileActive, tuilesPosees, matriceTuiles, infoPion, mursVer, mursHor, matriceTerrain)

    elif entreeClavier == touchesDeBase[3]['elfe'][1] and nb_joueurs == 3 and modeTelekinesie == [1] and telekinesiesRestantes[0] > 0:
        selectTuileTelekinesie(telekinesieIndexTuileActive, tuilesPosees, matriceTuiles, infoPion, mursVer, mursHor, matriceTerrain)

    elif entreeClavier == touchesPartie['vortex'][0][1] and modeVortex == [1]:
        selectVortex(vortexActif, dicVortex, pionActif[touchesPartie['vortex'][1]])

    elif entreeClavier == touchesPartie['exploration'][0]:
        pionSurExploration(matriceTerrain, matriceTuiles, mursVer, mursHor, infoPion, tuilesRestantes, dicEsc, dicTuile2, dicTuile7, dicVortex, tuilesPosees, True, telekinesieIndexTuileActive, modeTelekinesie, telekinesiesRestantes)

    elif entreeClavier == 'w':
        debugActif *= -1
        
    elif entreeClavier == 'x':
        vitesse = vitesse**(-1)
        
    elif entreeClavier == 'twosuperior':
        tempsPause = pause()
        return tempsPause
    
    elif entreeClavier == 'BackSpace':
        sauvegarderPartie(matriceTerrain, infoPion, nb_joueurs, sortieActive, tempsRestant, touchesPartie, touchesPartieParJoueur, listeGagnants, matriceTuiles, mursVer, mursHor, tuilesPosees, dicVortex, dicEsc, telekinesiesRestantes)
    
    elif entreeClavier == 'Escape':
        tk.ferme_fenetre()

    return 0

def escalier(numeroPion, dicEsc, infoPion, listeGagnants):
    """Transporte un pion au bon endroit lors de l'usage d'un escalier"""
    if infoPion[numeroPion][0] not in dicEsc.values():
        return

    # Liste des positions occupées
    valeursDico = list(infoPion.values())
    positionOccupee = [valeursDico[i][0] for i in range(len(valeursDico)) if i + 1 not in listeGagnants]

    # Vérification que la case n'est pas occupée
    if dicEsc[infoPion[numeroPion][0]] in positionOccupee:
        infoPion[numeroPion][1] = infoPion[numeroPion][0]
        return

    # Si toutes les conditions sont validées, on effectue le changement de position
    infoPion[numeroPion] = [dicEsc[infoPion[numeroPion][0]], infoPion[numeroPion][0]]
    return

def activerVortex(numeroPion, dicVortex, infoPion, modeVortex, vortexActif, listeGagnants = []):
    """Active le "mode vortex" à l'aide de la touche v pendant lequel il est possible de choisir un vortex.
    Si un vortex a été choisi avec selectVortex(), on se téléporte à la bonne position.
    Sinon, il ne se passe rien et on sort du mode vortex."""
    if modeVortex == [0]:
        modeVortex[0] = 1
        selectVortex(vortexActif, dicVortex, numeroPion)
        return

    if modeVortex == [1] and vortexActif == [0]:
        modeVortex[0] = 0
        return

    if vortexActif != [0]:
        # Liste des positions occupées
        valeursDico = list(infoPion.values())
        positionOccupee = [valeursDico[i][0] for i in range(len(valeursDico)) if i + 1 not in listeGagnants]
        # Vérification que la case n'est pas occupée
        if dicVortex[numeroPion][vortexActif[0]-1] in positionOccupee:
            infoPion[numeroPion][1] = infoPion[numeroPion][0]
            return
        # Si toutes les conditions sont validées, on effectue le changement de position
        infoPion[numeroPion] = [dicVortex[numeroPion][vortexActif[0]-1], infoPion[numeroPion][0]]
        # On remet à 0 les variables des vortex
        modeVortex[0] = 0
        vortexActif[0] = 0
        return

def selectVortex(vortexActif, dicVortex, numeroPion):
    """En appuyant sur la touche b, on fait rouler le vortex sur lequel on souhaite se téléporter. En appuyant deux fois, on revient à 0, ce qui permet de ne pas se téléporter."""
    vortexActif[0] = (vortexActif[0] + 1) % (len(dicVortex[numeroPion]) + 1)
    return

def activerModeTelekinesie(infoPion, telekinesieIndexTuileActive, tuilesPosees, modeTelekinesie, matriceTerrain, matriceTuiles, mursVer, mursHor, tuilesRestantes, dicEsc, dic2, dic7, dicVortex, telekinesiesRestantes):
    """Active le mode de sélection de la case sur laquelle on veut utiliser la télékinésie"""
    if matriceTerrain[infoPion[3][0][0]][infoPion[3][0][1]] not in ('exp1', 'exp2', 'exp3', 'exp4'):
        return
    
    if modeTelekinesie == [0]:
        modeTelekinesie[0] = 1
        selectTuileTelekinesie(telekinesieIndexTuileActive, tuilesPosees, matriceTuiles, infoPion, mursVer, mursHor, matriceTerrain)
        return

    if modeTelekinesie == [1] and telekinesieIndexTuileActive == [0]:
        modeTelekinesie[0] = 0
        return

    if telekinesieIndexTuileActive != [0]:
        pionSurExploration(matriceTerrain, matriceTuiles, mursVer, mursHor, infoPion, tuilesRestantes, dicEsc, dic2, dic7, dicVortex, tuilesPosees, False, telekinesieIndexTuileActive, modeTelekinesie, telekinesiesRestantes)
        modeTelekinesie[0] = 0
        return

def selectTuileTelekinesie(telekinesieIndexTuileActive, tuilesPosees, matriceTuiles, infoPion,  mursVer, mursHor, matriceTerrain):
    """Passe à la case suivante lors du choix pendant la télékinésie"""
    telekinesieIndexTuileActive[0] = telekinesieIndexTuileActive[0]+1 if len(tuilesPosees) > telekinesieIndexTuileActive[0]+1 else 0
    
    if not tuileValide(tuilesPosees[telekinesieIndexTuileActive[0]], int(matriceTuiles[infoPion[3][0][0]][infoPion[3][0][1]][0]), infoPion, matriceTuiles, tuilesPosees, matriceTerrain, mursVer, mursHor):
        selectTuileTelekinesie(telekinesieIndexTuileActive, tuilesPosees, matriceTuiles, infoPion,  mursVer, mursHor, matriceTerrain)
    return

def miniTuile(matriceTuiles):
    """Fournit la matrice simplifiée déduite de matriceTuiles"""
    mini = [['$' for i in range(14)] for j in range(14)]
    for ligneMini in range(len(mini)):
        for colonneMini in range(len(mini[0])):
            ligneGrand =  (ligneMini*4)+colonneMini-7
            colonneGrand = (colonneMini*4)-ligneMini+5
            
            if 0 <= ligneGrand < 50 and 0 <= colonneGrand < 50:
                if matriceTuiles[ligneGrand][colonneGrand] != '$':
                    mini[ligneMini][colonneMini] = matriceTuiles[ligneGrand][colonneGrand]
    return mini

def detecterIntegrite(miniMatrice, positionASuppr, nbTuilesPosees):
    """Evalue si le fait de retirer une tuile du terrain le coupe en 2 ou non"""
    casesVisitees = set()
    matriceTronquee = list(map(list, miniMatrice))
    matriceTronquee[positionASuppr[0]][positionASuppr[1]] = "$"
    nbTuilesApres = len(detecterIntegriteRec(matriceTronquee, 6, 6, casesVisitees))
    if (nbTuilesPosees - 1) == nbTuilesApres:
        return True, casesVisitees
    return False, 0

def detecterIntegriteRec(matrice,i, j, casesVisitees):
    """Fonction recursive associée à la fonction précédente"""
    casesVisitees.add((i, j))
    for (p, q) in {(i - 1, j), (i, j + 1), (i + 1, j), (i, j - 1)}:
        if p in range(0, len(matrice)) and q in range(0, len(matrice[0])):
            if matrice[p][q] != "$" and (p, q) not in casesVisitees:
                detecterIntegriteRec(matrice, p, q, casesVisitees)
    return casesVisitees

def tuileAccessible(idTuile, ensembleTuile, matriceTerrain, matriceTuiles, mursVer, mursHor):
    """indique si la tuile possède au moins un accès à une tuile de l'ensemble"""
    # Commencons par trouver les coordonnées de la tuile idTuile
    HG = None
    for ligne in range(len(matriceTuiles)):
        for colonne in range(len(matriceTuiles)):
            if matriceTuiles[ligne][colonne] != "$":
                if int(matriceTuiles[ligne][colonne][0]) == idTuile and HG == None:
                    HG = (ligne, colonne)
    
    # Déduisons-en les coordonnées des sorties :
    listeSortie = [[0, 2], [2, 3], [3, 1], [1, 0]]
    for i in range(len(listeSortie)):
        listeSortie[i][0] += HG[0]
        listeSortie[i][0] += HG[1]
    
    # trouvons les coordonnées des murs correspondant dans leur matrices respectives
    listeMurSortie = [[0, 0], [0, 1], [1, 0], [0, 0]]
    for i in range(len(listeMurSortie)):
        listeMurSortie[i][0] += listeSortie[i][0]
        listeMurSortie[i][1] += listeSortie[i][1]
        
    # trouvons les coordonnées des cases derrière les murs respectivment
    listeCaseSortie = [[-1, 0], [0, 1], [1, 0], [0, -1]]
    for i in range(len(listeMurSortie)):
        if listeCaseSortie[i][0]+listeSortie[i][0] in range(0,50):
            listeCaseSortie[i][0] += listeSortie[i][0]
        else:
            listeCaseSortie[i][0] = 0
        if listeCaseSortie[i][1]+listeSortie[i][1] in range(0,50):
            listeCaseSortie[i][1] += listeSortie[i][1]
        else:
            listeCaseSortie[i][1] = 0
        
    # trouvons les id des Tuiles de listeCaseSortie
    listeIdTuiles = [0]*4
    for i, coor in enumerate(listeCaseSortie):
        if coor != 0:  
            ligne, colonne = coor
            if matriceTuiles[ligne][colonne][0] != '$':
                listeIdTuiles[i] = int(matriceTuiles[ligne][colonne][0])
            else :
                listeIdTuiles[i] = '$'
    
    # trouvons lesquelles de ces cases sont accessibles
    listeConnection = list()
    for i in range(len(listeMurSortie)):
        if not i%2:
            if not mursHor[listeMurSortie[i][0]][listeMurSortie[i][1]]:
                listeConnection.append(listeIdTuiles[i])
        else:
            if not mursVer[listeMurSortie[i][0]][listeMurSortie[i][1]]:
                listeConnection.append(listeIdTuiles[i])
    
    for elem in listeConnection:
        if not elem in ensembleTuile:
            listeConnection.remove(elem)
    
    if len(listeConnection) > 0:
        return True
    return False
    
                        

def tuileValide(tuileAValider, tuileDActivation, infoPion, matriceTuiles, tuilesPosees, matriceTerrain, mursVer, mursHor):
    """
    Prend une tuile en entrée et renvoie True ou False si on a le droit ou non d'utiliser la télékinésie dessus
    """
    if tuileAValider == tuileDActivation:
        return False
    
    if tuileAValider == 0:
        return True
    
    if tuileAValider == 1:
        return False
    
    # Vérif que la case est vide
    sequence = [i for i in range(1,8)]
    if pionSurTuile(matriceTuiles, sequence, tuileAValider, infoPion):
        return False
    
    # Vérification qu'on ne coupe pas le terrain
    # étape 1 au niveau des tuiles (continuité)
    tuilesContinue = False
    miniMatriceTuile = miniTuile(matriceTuiles)
    
    # for i in range(len(miniMatriceTuile)):
    #     print(miniMatriceTuile[i])
    
    # Trouvons les coordonnées de la tuile dans la mini matrice
    for ligne in range(len(miniMatriceTuile)):
        for colonne in range(len(miniMatriceTuile[0])):
            if miniMatriceTuile[ligne][colonne] != '$':
                #print("tuileAValider =", tuileAValider)
                if int(miniMatriceTuile[ligne][colonne][0]) == tuileAValider:
                    coor = (ligne, colonne)
                    # print("coor",coor)
    tuilesContinue, ensembleCoorTuile = detecterIntegrite(miniMatriceTuile, coor, len(tuilesPosees)-1)
    if not tuilesContinue:
        return False
    
    # # au niveau des murs
    # # création de l'ensembleTuile
    # ensembleTuile = set()
    # for elem in ensembleCoorTuile:
    #     ensembleTuile.add(int(miniMatriceTuile[elem[0]][elem[1]][0]))
    
    # for tuile in ensembleTuile:
    #     connection = tuileAccessible(tuile, ensembleTuile, matriceTerrain, matriceTuiles, mursVer, mursHor)
    #     if not connection:
    #         print("tuile non accessible", tuileAValider)
    #         return False
    
    return True
    
def telekinesie(matriceTerrain, matriceTuiles, idTuile, dicEsc, dicVortex, telekinesiesRestantes):
    """Modifie la matriceTerrain et la matriceTuile de manière à réaliser 
    l'action de télékinésie en supprimmant l'ancienne position de la tuile déplacée"""
    # On commence par rechercher la position (HG) de la tuile à déplacer dans matriceTuile
    telekinesiesRestantes[0] = telekinesiesRestantes[0] - 1
    HG = None
    for ligne in range(len(matriceTuiles)):
        for colonne in range(len(matriceTuiles[0])):
            if matriceTuiles[ligne][colonne][0] != "$":
                if int(matriceTuiles[ligne][colonne][0]) == idTuile and HG == None:
                    HG = (ligne, colonne)
                    break
    # Ensuite, il nous faut extraire les données de cette tuile (elle est supposée vide de pions)
    for ligne in range(4):
        for colonne in range(4):
            if type(matriceTerrain[ligne+HG[0]][colonne+HG[1]]) is str:
                if matriceTerrain[ligne+HG[0]][colonne+HG[1]][:-1] == 'vortex':
                    dicVortex[int(matriceTerrain[ligne+HG[0]][colonne+HG[1]][-1])].remove((ligne+HG[0], colonne+HG[1]))
            matriceTerrain[ligne+HG[0]][colonne+HG[1]] = None
            matriceTuiles[ligne+HG[0]][colonne+HG[1]] = "$"
            if (ligne+HG[0], colonne+HG[1]) in dicEsc.keys():
                dicEsc.pop((ligne+HG[0], colonne+HG[1]))
    
def pionSurTuile(matriceTuiles, sequencePion, idTuile, infoPion):
    """renvoie True si l’un des pions de la sequence se trouve sur la Tuile idTuile"""
    # Trouvons la position HG de la tuile
    if idTuile == 0:
        return False
    HG = None
    for ligne in range(len(matriceTuiles)):
        for colonne in range(len(matriceTuiles)):
            if matriceTuiles[ligne][colonne][0] != "$":
                a = int(matriceTuiles[ligne][colonne][0])
                if a == idTuile and HG == None:
                    HG = (ligne, colonne)
                    break
    # Regardons maintenant si un pion se trouve sur cette tuile
    for pion in sequencePion:
        if pion in infoPion.keys():
            positionPion = infoPion[pion][0]
            if HG[0] <= positionPion[0] and positionPion[0] <= HG[0]+3 and HG[1] <= positionPion[1] and positionPion[1] <= HG[1]+3:
                return True
    return False

def finPartie(partieGagnee, partiePerdue):
    """Affichage de l'écran de fin"""
    
    if partiePerdue:
        tk.efface('chronometre')
        tk.texte(100, 100, "Temps écoulé", taille = 30, couleur = 'red')
        tk.mise_a_jour()
    
    if partieGagnee:
        tk.efface('sortie')
        tk.efface('chronometre')
        tk.texte(100, 100, "Vous avez gagné !", taille = 30, couleur = 'light green')
        tk.mise_a_jour()

def verifVictoire(listeGagnants):
    """Renvoie True si la partie est gagnée"""
    if len(listeGagnants) == 4:
            sleep(1)
            return True
    return False

def sauvegarderPartie(matriceTerrain, infoPion, nb_joueurs, sortieActive, tempsRestant, touchesPartie, touchesPartieParJoueur, listeGagnants, matriceTuiles, mursVer, mursHor, tuilesPosees, dicVortex, dicEsc, telekinesiesRestantes):
    """ Sauvegarde et quitte la partie """
    with open("save.txt", "w") as save:
        # Enregistrement matriceTerrain
        for i in range(len(matriceTerrain)):
            ligne = []
            for element in matriceTerrain[i]:
                ligne.append(str(element))
            save.write(" ".join(ligne)+"\n")
        save.write("\n")
        
        # Enregistrement infoPion
        data_infoPion = infoPion.items()
        for cleValeur in data_infoPion:
            ligne = []
            ligne.append(str(cleValeur[0]))
            for couple in cleValeur[1]:
                chaine = []
                for element in couple:
                    chaine.append(str(element))
                chaine = ",".join(chaine)
                ligne.append(chaine)
            save.write(" ".join(ligne)+"\n")
        save.write('\n')
        
        # nb_joueurs, sortieActive, tempsRestant
        save.write(str(nb_joueurs)+"\n\n"+str(sortieActive)+"\n\n"+str(tempsRestant)+"\n")
        
        # touchesPartie
        data_touchesPartie = touchesPartie.items()
        for cleValeur in data_touchesPartie:
            ligne = []
            ligne. append(cleValeur[0])
            for valeur in cleValeur[1]:
                if valeur is tuple:
                    chaine = []
                    for element in valeur:
                        chaine.append(str(element))
                    chaine = ",".join(chaine)
                    ligne.append(chaine)
                else:
                    ligne.append(str(valeur))
            save.write(" ".join(ligne)+"\n")
        save.write('\n')
        
        # touchesPartieParJoueur
        data_touchesPartieParJoueur = touchesPartieParJoueur.items()
        for cleValeur1 in data_touchesPartieParJoueur:
            data_dico = cleValeur1[1].items()
            for cleValeur2 in data_dico:
                ligne = [str(cleValeur1[0])]
                ligne.append(str(cleValeur2[0]))
                ligne.append(str(cleValeur2[1]))
                save.write(' '.join(ligne)+'\n')
        save.write('\n')
        
        
        #listeGagnants
        for element in listeGagnants:
            save.write(str(element)+"\n")
        save.write('\n')
            
        # matriceTuiles
        for ligne in range(len(matriceTuiles)):
            chaine = ""
            for colonne in range(len(matriceTuiles)):
                chaine += matriceTuiles[ligne][colonne] + ' '
            chaine += '\n'
            save.write(chaine)
        save.write('\n')
                
        # mursVer
        for ligne in range(len(mursVer)):
            chaine = ''
            for colonne in range(len(mursVer[0])):
                chaine += str(mursVer[ligne][colonne])+' '
            chaine += '\n'
            save.write(chaine)
        save.write('\n')
        
        # mursHor
        for ligne in range(len(mursHor)):
            chaine = ''
            for colonne in range(len(mursHor[0])):
                chaine += str(mursHor[ligne][colonne])+' '
            chaine += '\n'
            save.write(chaine)
        save.write('\n')
        
        # tuilesPosees
        chaine = ''
        for element in tuilesPosees:
            chaine += str(element)+' '
        save.write(chaine)
        save.write('\n\n')
        
        # dicVortex
        for key, value in dicVortex.items():
            chaine = str(key)+':'
            for couple in value:
                chaine += str(couple[0])+','+str(couple[1])+' '
            chaine += '\n'
            save.write(chaine)
        save.write('\n')
        
        # dicEsc
        for key, value in dicEsc.items():
            chaine = str(key[0])+','+str(key[1])+':'+str(value[0])+','+str(value[1])+'\n'
            save.write(chaine)
            
        # telelekinesiesRestantes
        save.write('\n'+str(telekinesiesRestantes[0]))
            
                
        
    tk.ferme_fenetre()
        
def chargerPartie():
    """Charge la partie, de manière à pouvoir continuer la dernière sauvegarde"""
    with open('save.txt','r') as save:
        data_save = save.read()
        
    data_save = data_save.split('\n')
    
    # matriceTerrain
    compteur = 0
    while data_save[compteur] != '':
        compteur += 1 
    
    matriceTerrain = []
    for ligne in data_save[:compteur]:
        ligne = ligne.split(' ')
        for i in range(len(ligne)):
            if ligne[i] == '1' or ligne[i] == '0':
                ligne[i] = int(ligne[i])
            elif ligne[i] == 'None':
                ligne[i] = None
            else:
                ligne[i]
        matriceTerrain.append(ligne)
    
    # infoPion
    debut = compteur+1
    compteur += 1
    while data_save[compteur] != '':
        compteur += 1
    
    infoPion = dict()
    for ligne in data_save[debut:compteur]:
        ligne = ligne.split(' ')
        infoPion[int(ligne[0])] = [[int(ligne[1].split(',')[0]), int(ligne[1].split(',')[1])], [int(ligne[2].split(',')[0]), int(ligne[2].split(',')[1])]]
        
    # nb_joueurs, sortieActive, tempsRestant
    compteur += 1
    nb_joueurs = int(data_save[compteur])
    compteur += 2
    sortieActive = True if data_save[compteur] == 'True' else False
    compteur += 2 
    tempsRestant = float(data_save[compteur])
    compteur += 1 
    
    # touchesPartie 
    touchesPartie = dict()
    debut = compteur
    while data_save[compteur] != '':
        compteur += 1
    for ligne in data_save[debut:compteur]:
        ligne = ligne.split()
        if ligne[0] == 'vortex':
            touchesPartie.setdefault('vortex', None)
            touche = " ".join(ligne[1:3]).strip("(')").split("', '")
            touchesPartie["vortex"] = (tuple(touche), int(ligne[3]))
        else :
            touchesPartie[ligne[0]] = (ligne[1], int(ligne[2]))
            
    # touchesPartieParJoueur
    touchesPartieParJoueur = dict()
    compteur += 1
    debut = compteur
    while data_save[compteur] != '':
        compteur += 1
    for ligne in data_save[debut:compteur]:
        ligne = ligne.split()
        if ligne[1] == 'vortex' :
            if touchesPartieParJoueur.get(int(ligne[0])) == None:
                touchesPartieParJoueur.setdefault(int(ligne[0]), dict())
            touchesPartieParJoueur[int(ligne[0])]['vortex'] = tuple(" ".join(ligne[2:4]).strip("(')").split("', '"))
        
        elif ligne[1] == 'elfe' :
            if touchesPartieParJoueur.get(int(ligne[0])) == None:
                touchesPartieParJoueur.setdefault(int(ligne[0]), dict())
            touchesPartieParJoueur[int(ligne[0])]['elfe'] = tuple(" ".join(ligne[2:4]).strip("(')").split("', '"))
            
        else:
            if touchesPartieParJoueur.get(int(ligne[0])) == None:
                touchesPartieParJoueur.setdefault(int(ligne[0]), dict())
            touchesPartieParJoueur[int(ligne[0])][ligne[1]] = ligne[2]
    compteur += 1        
    
    # listeGagnants
    listeGagnants = list()
    debut = compteur
    while data_save[compteur] != '':
        compteur += 1
    for ligne in data_save[debut:compteur]:
        if ligne != '':
            listeGagnants.append(int(ligne))
    compteur += 1
    
    # matriceTuiles
    matriceTuiles = []
    debut = compteur
    while data_save[compteur] != '':
        compteur += 1
    for ligne in data_save[debut:compteur]:
        ligne = ligne.strip().split(' ')
        matriceTuiles.append(ligne)
    compteur += 1
    
    
    # mursVer
    mursVer = list()
    debut = compteur
    while data_save[compteur] != '':
        compteur += 1
    for ligne in data_save[debut:compteur]:
        ligne =  list(map(lambda x: int(x), ligne.strip().split()))
        mursVer.append(ligne)
    compteur += 1
    
    
    # mursHor
    mursHor = list()
    debut = compteur
    while data_save[compteur] != '':
        compteur += 1
    for ligne in data_save[debut:compteur]:
        ligne = list(map(lambda x: int(x), ligne.strip().split()))
        mursHor.append(ligne)
    compteur += 1
    
    # tuilesPosees
    tuilesPosees = list(map(lambda x: int(x) ,data_save[compteur].strip().split(' ')))
    compteur += 2
    
    
    # dicVortex
    debut = compteur
    while data_save[compteur] != '':
        compteur += 1
    dicVortex = dict()
    for ligne in data_save[debut:compteur]:
        ligne = ligne.strip().split(':')
        dicVortex.setdefault(int(ligne[0]), list())
        couples = ligne[1].split(' ')
        for duo in couples:
            nombre1 = int(duo.split(',')[0])
            nombre2 = int(duo.split(',')[1])
            dicVortex[int(ligne[0])].append((nombre1, nombre2))
    compteur += 1

    
    # dicEsc
    debut = compteur
    while data_save[compteur] != '':
        compteur += 1
    dicEsc = dict()
    for ligne in data_save[debut:compteur]:
        ligne = ligne.strip().split(':')
        liste = []
        for couple in ligne:
            couple = couple.split(',')
            nombre1 = int(couple[0])
            nombre2 = int(couple[1])
            liste.append((nombre1, nombre2))
        dicEsc[liste[0]] = liste[1]
    compteur += 1
    
    # telekinesiesRestantes
    telekinesiesRestantes = [int(data_save[compteur].strip())]
        
    return matriceTerrain, infoPion, nb_joueurs ,sortieActive , tempsRestant, touchesPartie, touchesPartieParJoueur, listeGagnants, matriceTuiles, mursVer, mursHor, tuilesPosees, dicVortex, dicEsc, telekinesiesRestantes
