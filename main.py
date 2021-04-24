
# -*- coding: utf-8 -*-
"""
Programme principal du jeu MagicMaze.
Auteurs : Théodore Garcher, Simon Eveillé

Programme à exécuter pour lancer une partie
"""

# IMPORTS ####################################################################

import upemtk as tk
from time import sleep
import random as rand
from moduleLogique import *
from moduleGraphique import *
from varMM import *

# DEFINITION DES FONCTIONS ###################################################

def main():
    """ Fonction principale """
    #### Définition des constantes et initialisation des variables ###########  
    
    # info sur le contenu des cellules 
    matriceTerrain, matriceTuiles, mursVer, mursHor = creerMatriceTerrain()
    tuilesRestantes = [i for i in range(2, 10)]

    infoPion = dict() # info sur la position des pion
    initPions(1, (24, 24), infoPion)
    initPions(2, (25, 25), infoPion)
    initPions(3, (25, 24), infoPion)
    initPions(4, (24, 25), infoPion)
    
    dicEsc = {
        (25, 26): (26, 25),
        (26, 25): (25, 26)
    }

    dicTuile2 = defDicTuile2()
    dicTuile7 = defDicTuile7()

    #initialisé à 0 (inactif), passe à 1 si actif
    #on utilise une liste car objet mutable (dégueux mais pratique)
    modeVortex = [0]

    #roulement entre 0 (aucun portail selectionné) et les autres portails accessibles
    vortexActif = [0]

    tuilesPosees = [0, 1]
    modeTelekinesie = [0]
    telekinesieIndexTuileActive = [0]
    telekinesiesRestantes = [2]

    dicVortex = {
        1: [(23, 26)],
        2: [(24, 26)],
        3: [(26, 23)],
        4: [(25, 23)]
    }

    sortieActive = False
    partiePerdue = False
    partieGagnee = False
    dureeTotalePartieInitiale = 180 # En secondes
    tempsRestant = dureeTotalePartieInitiale
    modifTemps = [0]


    listeGagnants = []
    
    debugActif = -1 # -1 -> vdésactivé ; 1 -> activé
    vitesse = 1/500 # Vitesse du mode debug
    
    #### Ouverture de la fenêtre #############################################
    
    tk.cree_fenetre(1900, 1000)
    
    #### Demander au joueur ce qu'il faut faire ##############################
    chargerSave = UIecranTitre()
    
    #### Choix du nombre de joueur ###########################################
    touchesDeBase = defTouchesDeBase()
    
    if not chargerSave:
        nb_joueurs = UIchoixNbrJoueur()
        touchesTotales = attributionDesTouches(nb_joueurs, touchesDeBase)
        touchesPartieParJoueur = touchesTotales[0]
        touchesPartie = touchesTotales[1]
        
    else:
        
        matriceTerrain, infoPion, nb_joueurs, sortieActive, tempsRestant, touchesPartie, touchesPartieParJoueur, listeGagnants, matriceTuiles, mursVer, mursHor, tuilesPosees, dicVortex, dicEsc, telekinesiesRestantes = chargerPartie()
        for tuile in tuilesPosees:
            if tuile in tuilesRestantes:
                tuilesRestantes.remove(tuile)
    pionActif = dict()
    for i in range(1, nb_joueurs+1):
        pionActif[i] = 1

    #### Entrée dans le jeu ##################################################
    
    heureDebut = time()
    dureeTotalePartie = tempsRestant
    
    
    while True: # Boucle Principale
        tempsPause = gestionEntreeClavier(matriceTerrain, mursVer, mursHor, infoPion, pionActif, sortieActive, debugActif, vitesse, listeGagnants, dicVortex, dicEsc, dicTuile2, dicTuile7, modeVortex, vortexActif, touchesPartie, touchesPartieParJoueur, nb_joueurs, touchesDeBase, tempsRestant, matriceTuiles, tuilesRestantes, tuilesPosees, telekinesieIndexTuileActive, modeTelekinesie, telekinesiesRestantes)
        heureDebut = heureDebut + tempsPause
        
        if not sortieActive: # Si les sorties ne sont pas activées on regarde si on peut les activer
            sortieActive = pionSurObjet(matriceTuiles, matriceTerrain, infoPion)
        
        # Mise à jour de l'image, gestion de la victoire/défaite
        tk.efface_tout()
        partiePerdue, tempsRestant = afficherPlateau(matriceTerrain, mursHor, mursVer, infoPion ,listeGagnants, pionActif, debugActif, sortieActive, heureDebut, dureeTotalePartie, modifTemps, vortexActif, dicVortex, touchesPartie, touchesPartieParJoueur, matriceTuiles, modeTelekinesie, tuilesPosees, telekinesieIndexTuileActive, telekinesiesRestantes)
        partieGagnee = verifVictoire(listeGagnants)
        if partieGagnee or partiePerdue:
            break
    
    # Affichage des messages de victoire/défaite
    finPartie(partieGagnee, partiePerdue)
    
    tk.attente_clic_ou_touche()
    tk.ferme_fenetre()
    
# MAIN #######################################################################

if __name__ == "__main__":
    main()
