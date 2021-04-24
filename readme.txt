Magic Maze

Simon Eveillé
Théodore Garcher

Ce qui a été implémenté :
* Un menu de sélection du nombre de joueurs (1 à 3) et donc par extension, un mode multijoueur.
* Une répartition des touches aléatoires entre les joueurs s’ils sont plusieurs, pour s’assurer que chaque partie soit différente. Il y a au total 7 touches d’actions à attribuer (4 déplacements, vortex, escalier, et exploration). Le nombre de touches d’actions étant premier, chaque joueur recevra un nombre aléatoire équitable d’actions (4 et 3 pour deux joueurs, 2 et 2 et 3 pour 3 joueurs).
* 4 pions de couleur controllables par le(s) joueur(s).
* Une panoplie de tuiles réalisées par nos soins sur Paint.net, en essayant de rester le plus fidèle possible au jeu de base.
* Un chronomètre qui s’active dès le début de la partie ; s’il arrive à 0 la partie est perdue !
* Une interface graphique sur laquelle on peut voir les pions, les tuiles, ainsi que les informations annexes qui peuvent aider le joueur : quel est le pion sélectionné, combien de temps me reste-t-il avant de perdre, quelles sont mes touches, etc.
* Des restrictions quant aux déplacements possibles par les pions : on ne peut pas passer à travers un mur, sortir d’une tuile, se déplacer sur la même case qu’un autre pion.
* Des cases sablier qui permettent comme l’objet physique de renverser le temps qu’il reste (ce qui peut provoquer une diminution effective du temps restant si mal utilisé !)
* Un système d’escaliers utilisables uniquement par le joueur possédant l’action éponyme.
* Un système de vortex utilisables uniquement par le joueur possédant l’action éponyme. Le vortex fonctionne de la façon suivante : on appuie sur une touche 1 pour activer le mode vortex, puis on appuie sur une deuxième touche 2 pour effectuer un roulement entre les différents vortex accessibles. On peut quitter ce mode vortex et ne pas se téléporter en ne sélectionnant aucun vortex à l’aide de la touche 2, puis en sortant du mode vortex avec la touche 1.
* Des cases exploration disposées sur chaque tuile et qui permettent de disposer sur le plateau des tuiles aléatoires piochées. Les tuiles s’orientent automatiquement dans le bon sens.
* Lorsque les 4 pions sont sur leur case objet respective, la sortie s’active et les pions peuvent l’emprunter. Si tous les pions l’empruntent avant la fin du chronomètre, la partie est gagnée.
* L’extension des gardes : un garde est placé sur la tuile 9 lors de sa découverte et de son ajout au plateau. Un garde ne peut pas se trouver sur la même tuile que les autres pions joueurs. Les joueurs avec les actions de déplacement correspondantes peuvent déplacer le garde. Deux nouveaux gardes de renfort sont disposés sur le plateau lorsque la sortie est activée !
* L’extension de la télékinésie de l’elfe : 2 fois maximum par partie, le pion vert (l’elfe) peut déplacer une tuile éligible devant lui lorsqu’il se trouve sur une case exploration non utilisée. Les tuiles éligibles sont les tuiles qui ont déjà été posées sur le plateau et qui respectent certaines conditions (pas de pion sur la tuile, ne pas pouvoir déplacer la tuile sur laquelle on se trouve, ne pas pouvoir déplacer la tuile initiale, et ne pas pouvoir scinder le plateau en deux zones distinctes).
* Un système de caméra qui permet de recentrer automatiquement le plateau au centre de l’écran lorsqu’un certain nombre de tuiles posées a été atteint. Cela permet d’éviter au plateau de “sortir” de l’écran.
* Un mode debug dont on peut modifier la vitesse et qui fait bouger automatiquement tous les pions.
* Mettre la partie sur pause en appuyant sur ².
* La possibilité de sauvegarder une partie en appuyant sur la barre espace, de fermer le programme, puis de charger la partie.
Ce qui n’a pas été implémenté ou ce qui a été retiré :
* Des animations pour le déplacement des pions, retirées à cause de problèmes techniques (upemtk gère mal la suppression d’un trop grand nombre d’images)
* Un affichage plus graphique pour le sablier (toujours à cause d’upemtk)
* Une fonction récursive plus poussée pour s’assurer qu’en utilisant la télékinésie, on ne rend pas des morceaux du plateau inaccessibles. Pour le moment, la fonction récursive ne gère pas une situation gênante : le plateau est continu (il n’a pas été séparé en deux, les tuiles sont toujours adjacentes les unes aux autres) mais il a été séparé dans le sens où il n’y a aucun passage permettant de passer d’un côté à l’autre du plateau.


Choix techniques, structure de données :
Le programme est divisé en 3 parties, en plus des différents fichiers de texture :
* main.py : contient le script de déroulement du jeu
* moduleLogique.py : contient les différentes fonctions de gestion du plateau et des pions 
* moduleGraphique.py : contient les différentes fonctions d’affichage
* varMM.py : contient des dictionnaires et matrices volumineux utilisés dans le reste du programme

Structure de données :
* L’objet qui décrit le plateau est une matrice nommée matriceTerrain de taille 50 par 50. La tuile initiale (tuile n°1) de taille 4 par 4 est positionnée au centre de matriceTerrain. A chaque ajout de tuile, on vient positionner au bon endroit à l’aide de plusieurs fonctions les tuiles à ajouter en alignant entrées et sorties entre chaque tuile, avec rotation si besoin est. Chaque case de la matrice est codée en fonction de l’information qu’elle contient (case vide, case accessible, vortex, escalier…).
* Les murs verticaux et horizontaux sont respectivement contenus dans  les matrices mursVer et mursHor, respectivement. Ces matrices indiquent la présence de murs par des 1 et leur absence par des 0. Par exemple, un mur en haut de la cellule en 0-0 indique que la matice mursHor contient un 1 en 0-0
* Le programme garde en mémoire la manière dont ont été déposées les tuiles dans une matrice nommée matriceTuiles. Elle est de même taille que la matrice matriceTerrain. Ici, l’absence de tuile est noté ‘$’, et lorsqu’il y a une tuile la valeur correspondante est une chaîne de caractère contenant  l’id de la tuile (de 1 à 9) et son orientation (de 0 à 3 ) pour haut, droite, bas, gauche
* L’objet qui décrit la position des joueurs ; le dictionnaire infoPion :
Il est de la forme { numeroPion : [(ligneActuelle, colonneActuelle), (lignePrécédente, positionPrécédente)] }
Autrement dit, ce dictionnaire contient les positions actuelle et précédente d’un pion. La position précédente a été implémentée afin d’afficher une animation de pion qui se déplace lorsqu’on déplace un pion, mais nous n’avons pas pu rendre cette fonctionnalité entièrement opérationnelle étant donné certains comportemenst de upemtk avec la supressions de trop nombreux tags, ce pourquoi nous avons décidé de rendre le projet sans cette fonctionnalité au moins pour la phase 1.$
* pionActif : un dictionnaire qui décrit pour chaque joueur le pion qui est actuellement sélectionné
* listeGagnants : liste des pions ayant gagné (à valeurs dans les entiers de 1 à 4)
* dureeTotalePartieInitiale : durée en secondes de la partie (au début)
* dicEsc : un dictionnaire qui répertorie les couples de cases escaliers. Chaque escalier correspond à deux couples clé : valeur tel que {tupleCoordonnées1 : tupleCoordonnées2,  tupleCoordonnées2 : tupleCoordonnées1}, ce qui permet de récupérer facilement les coordonnées de l’escalier correspondant peu importe dans quel sens on le prend.
* dicVortex : un dictionnaire dont les couples clé : valeurs sont enregistrées sous la forme {n° joueur : [liste des tuples de coordonnées des vortex accessibles]
* modeVortex : permet de savoir si un joueur a activé le mode vortex (valeur égale à 1 ou 0)
* vortexActif : vortex actuellement sélectionné dans le roulement des vortex accessibles
* tuilesPosees : liste des numéros des tuiles posées jusqu’ici sur le plateau
* modeTelekinesie : comme pour le vortex, valeur égale à 0 ou 1 qui indique si le joueur a activé ou non le mode télékinésie
* telekinesieIndexTuileActive : stocke un index permet de récupérer la tuile en ce moment sélectionnée par le joueur dans le roulement des tuiles posées à sa disposition lors de l’utilisation de la télékinésie
* telekinesiesRestantes : nombre restant d’utilisations de la télékinésie


Problèmes rencontrés et solutions apportées :
L’animation des pions et d’une ‘barre de temps’ créaient des problèmes liés à upemtk et à la suppression de trop nombreux tags. Pour ce problème, la solution a été de retourner en arrière et de retirer les animations après avoir testé d’autres solutions comme, la réinitialisation régulière de l’affichage, qui avait pour problème d’afficher un écran blanc pendant une fraction de seconde, ou alors la création de tags ‘uniques’ pour chaque image de chaque animation, qui n’a pas non plus réglé le problème.


L’organisation du travail a deux n’a pas été évidente au début (nous allons pour la phase 2 essayer d’utiliser Git et Github). Une fois les premières versions stables développées, il nous était cependant possible de travailler en parallèle sans se “marcher dessus”.


Nous avons à plusieurs endroits du programme eu besoin de variables globales, mais nous ne savions pas comment les modifier. Nous avons fini par utiliser des listes (objets mutables) pour pouvoir modifier dans des fonctions certaines variables importantes pour l’ensemble du programme.


Un défaut d’organisation et une mauvaise anticipation de la charge de travail nous a enfin empêché de construire l'extension liée à la télékinésie comme nous le voulions.