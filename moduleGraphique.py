"""
Module graphique du jeu MagicMaze.
Auteurs : Théodore Garcher et Simon Eveillé

Contient les fonctions permettant l'affichage du jeu à l'écran
"""
# IMPORTS ####################################################################

import upemtk as tk
from time import time
from moduleLogique import pionSurSablier

# DEFINITION DES FONCTIONS ###################################################

def conversionCoordonnee(position, matriceTuiles):
    """
    Convertit des positions de cellule sur la matrice Terrain en positions de
    pixels réelles sur l'image à afficher

    Args:
        position (tuple): (ligne, colonne)

    Returns:
        positionReelle (tuple): (ligne, colonne)

    """
    ### Calculons la hauteur, et la largeur du plateau utilisée, trouvons
    ### aussi la position de la case tout en haut à gauche
    
    # haut
    haut = None
    for ligne in range(len(matriceTuiles)):
        for colonne in range(len(matriceTuiles[0])):
            if matriceTuiles[ligne][colonne] != '$' and haut == None:
                haut = ligne
            
    # bas
    bas = None
    for ligne in range(len(matriceTuiles)-1, -1, -1):
        for colonne in range(len(matriceTuiles[0])):
            if matriceTuiles[ligne][colonne] != '$' and bas == None:
                bas = ligne
    
    
    #gauche
    gauche = None
    for colonne in range(len(matriceTuiles[0])):
        for ligne in range(len(matriceTuiles)):
            if matriceTuiles[ligne][colonne] != '$' and gauche == None:
                gauche = colonne
    
    #droite
    droite = None
    for colonne in range(len(matriceTuiles[0])-1, -1, -1):
        for ligne in range(len(matriceTuiles)):
            if matriceTuiles[ligne][colonne] != '$' and droite == None:
                droite = colonne
                
    # On peut maintenant déduire commet décaler les textures en fonctions des
    # bornes du terrain
    hauteur = bas-haut+1
    largeur = droite-gauche+1
    
    decalGauche = -((gauche+(largeur/2)-25))*40
    decalHaut = -((haut+(hauteur/2)-25))*40
    listeElement = []
    for ligne in matriceTuiles:
        for element in ligne:
            if element != "$" and element not in listeElement:
                listeElement.append(element)
    if len(listeElement) < 4:
        decalGauche = 0
        decalHaut = 0
    ligne = position[0]
    colonne = position[1]
    
    ligne = (ligne*40)+decalHaut-470
    colonne = (colonne*40)+decalGauche-335
    return ligne, colonne

def conversionCoordonneesMurHor(position):
    """Convertie un tuple de coordonnées de plateau en coordonnées en pixels"""
    ligne = position[0]
    colonne = position[1]
    
    ligne = (ligne*40)-476
    colonne = (colonne*40)-576
    return ligne, colonne

def conversionCoordonneesMurVer(position):
    """Convertie un tuple de coordonnées de plateau en coordonnées en pixels"""
    ligne = position[0]
    colonne = position[1]
    
    ligne = (ligne*40)-499
    colonne = (colonne*40)-556
    return ligne, colonne

def UIecranTitre():
    """ Affiche l'écran titre, renvoie True si le joueur charge un ancienne partie, sinon False"""
    tk.texte(800, 100, 'MagicMaze, par Théodore Garcher et Simon Eveillé', ancrage = 'center')
    tk.rectangle(200, 200, 550, 350, couleur = 'black', remplissage = '#b9b9b9', epaisseur = 3)
    tk.texte(375, 275, "Nouvelle Partie", ancrage = 'center')
    tk.rectangle(200, 400, 550, 550, couleur = 'black', remplissage = '#b9b9b9', epaisseur = 3)
    tk.texte(375, 475, "Charger une partie",  ancrage = 'center')
    tk.texte(800, 800, "Selectionnez le nombre de joueur avec ↑, ↓ et Entrée", ancrage = 'center' )
    
    
    
    # Selecteur
    choix = False
    entreeClavier = None
    while entreeClavier != 'Return':
        tk.efface('selecteur')
        if not choix :
            tk.rectangle(190, 190, 560, 360, couleur = '#565656', remplissage = '', epaisseur = 4, tag = 'selecteur')
        else :
            tk.rectangle(190, 390, 560, 560, couleur = '#565656', remplissage = '', epaisseur = 4, tag = 'selecteur')
        entreeClavier = tk.attente_touche()
        
        if entreeClavier == 'Up':
            choix = False
        elif entreeClavier == 'Down':
            choix = True
    
    return choix
    
    

def UIchoixNbrJoueur():
    """ Renvoie le nombre de joueur selectionné par l'utilisateur """
    # Affichage de base
    tk.efface_tout()
    tk.texte(600, 100, "Selectionnez le nombre de joueur avec ↑, ↓ et Entrée", ancrage = 'center' )
    tk.rectangle(200, 200, 450, 350, couleur = 'black', remplissage = '#b9b9b9', epaisseur = 3)
    tk.texte(325, 280, "1", ancrage = 'center', taille = 30)
    tk.rectangle(200, 400, 450, 550, couleur = 'black', remplissage = '#b9b9b9', epaisseur = 3)
    tk.texte(325, 480, "2", ancrage = 'center', taille = 30)
    tk.rectangle(200, 600, 450, 750, couleur = 'black', remplissage = '#b9b9b9', epaisseur = 3)
    tk.texte(325, 680, "3", ancrage = 'center', taille = 30)
    
    # Selecteur
    choix = 1
    entreeClavier = None
    
    while entreeClavier != 'Return':
        tk.efface('selecteur')
        if choix == 1:
            tk.rectangle(190, 190, 460, 360, couleur = '#565656', remplissage = '', epaisseur = 4, tag = 'selecteur')
        elif choix == 2:
            tk.rectangle(190, 390, 460, 560, couleur = '#565656', remplissage = '', epaisseur = 4, tag = 'selecteur')
        elif choix == 3:
            tk.rectangle(190, 590, 460, 760, couleur = '#565656', remplissage = '', epaisseur = 4, tag = 'selecteur')
        
        entreeClavier = tk.attente_touche()
        
        if entreeClavier == 'Up':
            choix = choix-1 if choix > 1 else choix
        if entreeClavier == 'Down':
            choix = choix+1 if choix < 3 else choix
    return choix
    
    
    
    entree = None
    while entree != 'Escape':
        entree = tk.attente_touche()
    return

def affichageMurs(mursHor, mursVer):
    """Affiche tous les murs à leur emplacement sur le plateau"""
    # Murs horizontaux
    for ligne in range(len(mursHor)):
        for colonne in range(len(mursHor[0])):
            if mursHor[ligne][colonne]:
                ligneP, colonneP = conversionCoordonneesMurHor((ligne, colonne))
                tk.image(colonneP, ligneP, "murHor.gif")
    
    # Murs verticaux
    for ligne in range(len(mursVer)):
        for colonne in range(len(mursVer[0])):
            if mursVer[ligne][colonne]:
                ligneP, colonneP = conversionCoordonneesMurVer((ligne, colonne))
                tk.image(colonneP, ligneP, "murVer.gif")
            

def afficherPion(numeroPion, infoPion, matriceTuiles):
    """
    Affiche au bon emplacement le joueur choisi

    Args:
        numeroPion (int): entre 1 et 4
        infoPion (dict): dictionnaire d'info sur la position des pions
        animation (bool): False --> désactive les animations
        
    Returns:
        None.

    """
    
    positionFinale = infoPion[numeroPion][0]
    positionFinale = conversionCoordonnee(positionFinale, matriceTuiles)
    
    listeImage = ['pionViolet.gif', 'pionJaune.gif', 'pionVert.gif', 'pionOrange.gif', 'garde.gif', 'garde.gif', 'garde.gif']
    
    tk.image(positionFinale[1], positionFinale[0], listeImage[numeroPion-1])
    

def affichagePionsInterface(touchesPartieParJoueur):
    """
    Affiche dans l'interface tous les pions jouables avec leurs couleurs associées
    """
    for cle in touchesPartieParJoueur.keys():
        for i, j in [(1, 'purple'), (2, 'gold2'), (3, 'green2'), (4, 'dark orange'), (5, 'grey'), (6, 'grey'), (7, 'grey')]:
            tk.cercle(1300+i*75, 50 + cle * 250, 20, 'black', j, 2)
    return


def affichagePionActif(pionActif):
    """
    Args :
        pionActif (int)
    Returns:
        None
    Affiche dans l'interface le pion selectionné
    """
    for joueur, pion in pionActif.items():
        tk.cercle(1300+pion*75, 50 + joueur * 250, 10, 'black', 'black', 2)
    return

def affichageVortexActif(pionActif, vortexActif, dicVortex, matriceTuiles):
    ligne, colonne = conversionCoordonnee(dicVortex[pionActif][vortexActif[0]-1], matriceTuiles)
    tk.image(colonne, ligne, 'vortexSelect.gif')

def affichageTouches(touchesPartieParJoueur):
    for joueur, touches in touchesPartieParJoueur.items():
        textetouches = 'Touches du joueur ' + str(joueur) + ' :\n'
        for cle, valeur in touches.items():
            textetouches += cle + ' : ' + str(valeur) + '\n'
        tk.texte(1480, 100 + 250 * joueur, textetouches, taille=15)

def affichageTuiles(matriceTuiles):
    """Affiche les tuiles sur le plateau"""
    tuile = set([str(i) for i in range(1, 10)])
    for ligne in range(len(matriceTuiles)):
        for colonne in range(len(matriceTuiles[0])):
            if matriceTuiles[ligne][colonne][0] in tuile:
                tuile.discard(matriceTuiles[ligne][colonne][0])
                Nligne, Ncolonne = conversionCoordonnee((ligne, colonne), matriceTuiles)
                tk.image(Ncolonne+60, Nligne+60, "tuile"+matriceTuiles[ligne][colonne]+".gif")
                
def affichageTelekinesie(tuilesPosees, telekinesieIndexTuileActive, telekinesiesRestantes):
    """Affiche la tuile selectionnée durant la télékinésie"""
    numTuile = str(tuilesPosees[telekinesieIndexTuileActive[0]])
    if numTuile == '0':
        numTuile = 'aucune'
    tk.texte(900, 10, "Télékinésie de l'elfe activée\nTuile sélectionnée : " + numTuile + "\nActivations restantes : " + str(telekinesiesRestantes[0]))

def afficherPlateau(matriceTerrain, mursHor, mursVer, infoPion ,listeGagnants, pionActif, debugActif, sortieActive, heureDebut, dureeTotalePartie, modifTemps, vortexActif, dicVortex, touchesPartie, touchesPartieParJoueur, matriceTuiles, modeTelekinesie, tuilesPosees, telekinesieIndexTuileActive, telekinesiesRestantes):
    """
    Affiche le terrain en entier et l'interface.

    Args:
        matriceTerrain (list): matrice qui encode le terrain
        infoPion (list): Infos de position des pions
        listeGagnants (list): liste des pions ayant gagné

    Returns:
        None.

    """
    #Calcul du temps restant
    tempsRestant = dureeTotalePartie-time()+heureDebut + modifTemps[0]
    tempsEcoule = dureeTotalePartie - tempsRestant
    # Renversement du sablier si un pion se trouve sur une case sablier
    if pionSurSablier(matriceTerrain, infoPion):
        if tempsRestant > tempsEcoule:
            modifTemps[0] += ((tempsRestant - tempsEcoule) * (-1))
        else:
            modifTemps[0] += (tempsEcoule - tempsRestant)
    

    # Affichage de l'interface
    tk.rectangle(0, 0, 1300, 1000, couleur = 'black', remplissage = 'grey')
    if debugActif == 1:
        tk.texte(180, 700, "Mode debug activé\nO: Changer la vitesse\nP: Quitter mode debug", taille = 28,couleur = 'red')
    if sortieActive:
        tk.texte(1320, 50, "Sortie activée ! Rendez vous à la sortie !", taille = 24, couleur = 'light green')
    tk.texte(10, 10, "Backspace : Sauvegarder et quitter")
    affichagePionsInterface(touchesPartieParJoueur)
    affichageTouches(touchesPartieParJoueur)
    affichagePionActif(pionActif)

    # Affichage du terrain et des pions
    # listeCoordonnee = [tuple([ligne, colonne]) for ligne in range(len(matriceTerrain)) for colonne in range(len(matriceTerrain[0]))]
    # affichageCellulePlateau(listeCoordonnee, matriceTerrain)
    # affichageMurs(mursHor, mursVer)
    affichageTuiles(matriceTuiles)
    for pion in range(1,8):
        if pion not in listeGagnants:
            if pion in infoPion.keys():
                afficherPion(pion, infoPion, matriceTuiles)
    if vortexActif != [0]:
        affichageVortexActif(pionActif[touchesPartie['vortex'][1]], vortexActif, dicVortex, matriceTuiles)
    if modeTelekinesie != [0]:
        affichageTelekinesie(tuilesPosees, telekinesieIndexTuileActive, telekinesiesRestantes)
    tk.mise_a_jour()
    
    # Gestion défaite
    if tempsRestant >= 0: # Partie en cours
        # Affichage du temps restant
        tk.efface('chronometre')
        tk.texte(1320, 10, str(int(tempsRestant))+" secondes restantes", taille = 24, tag = 'chronometre')
        return False, tempsRestant
        
    else: # Partie terminée
        return True, tempsRestant
