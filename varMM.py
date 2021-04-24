"""
Module variables du jeu MagicMaze.
Auteurs : Théodore Garcher et Simon Eveillé

Contient les fonctions relatives aux informations des tuiles à piocher, ainsi que différentes structures de données utiles au programme.
"""

def defDicTuile2():
    dico = {
        0: {
            (0, 2): (1, 0),
            (1, 0): (0, 2)
        },
        1: {
            (0, 2): (2, 3),
            (2, 3): (0, 2)
        },
        2: {
            (2, 3): (3, 1),
            (3, 1): (2, 3)
        },
        3: {
            (3, 1): (1, 0),
            (1, 0): (3, 1)
        }
    }
    return dico

def defDicTuile7():
    dico = {
        0: {
            (3, 1): (1, 2),
            (1, 2): (3, 1)
        },
        1: {
            (1, 0): (2, 2),
            (2, 2): (1, 0)
        },
        2: {
            (0, 2): (2, 1),
            (2, 1): (0, 2)
        },
        3: {
            (1, 1): (2, 3),
            (2, 3): (1, 1)
        }
    }
    return dico

def defTouchesDeBase():
    dico = {
        1: {
            "gauche": 'q',
            "droite": 'd',
            "haut": 'z',
            "bas": 's',
            "vortex": ('r', 't'),
            "escalier": 'e',
            "changerPion": 'a',
            "exploration": 'f',
            "elfe": ('c', 'v')
        },
        2: {
            "gauche": 'h',
            "droite": 'k',
            "haut": 'u',
            "bas": 'j',
            "vortex": ('o', 'p'),
            "escalier": 'i',
            "changerPion": 'y',
            "exploration": 'l',
            "elfe": (';', ':')
        },
        3: {
            "gauche": '4',
            "droite": '6',
            "haut": '8',
            "bas": '5',
            "vortex": ('plus', 'minus'),
            "escalier": '9',
            "changerPion": '7',
            "exploration": '1',
            "elfe": ('2', '3')
        }
    }
    return dico

def tuile1():
    matrice = [
        ['sablier', 1, 'exp4', 'vortex1'],
        ['exp1', 1, 1, 'vortex2'],
        ['vortex4', 1, 1, 'exp3'],
        ['vortex3', 'exp2', 1, 0],
    ]
    return matrice

def tuile1MursV():
    matrice = [
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0]
    ]
    return matrice

def tuile1MursH():
    matrice = [
        [1, 1, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 1, 0]
    ]
    return matrice

def tuile2():
    matrice = [
        [0, 0, 1, 1],
        ['exp4', 0, 0, 'sortie'],
        [1, 1, 0, 0],
        ['vortex3', 'expSortie', 'vortex1', 0],
    ]
    return matrice

def tuile2MursV():
    matrice = [
        [0, 0, 1, 0, 1],
        [0, 1, 0, 1, 1],
        [1, 0, 1, 0, 0],
        [1, 1, 0, 1, 0]
    ]
    return matrice

def tuile2MursH():
    matrice = [
        [0, 0, 1, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 1, 0]
    ]
    return matrice

def tuile3():
    matrice = [
        [1, 1, 'vortex4', 0],
        ['exp1', 1, 1, 'vortex3'],
        ['sablier', 1, 1, 'exp2'],
        [0, 'expSortie', 1, 0],
    ]
    return matrice

def tuile3MursV():
    matrice = [
        [1, 0, 1, 1, 0],
        [0, 1, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0]
    ]
    return matrice

def tuile3MursH():
    matrice = [
        [1, 1, 1, 0],
        [0, 0, 0, 1],
        [1, 0, 1, 1],
        [1, 1, 0, 1],
        [0, 0, 1, 0]
    ]
    return matrice

def tuile4():
    matrice = [
        [0, 0, 'exp1', 'vortex2'],
        [0, 'sablier', 1, 0],
        ['vortex4', 1, 1, 'exp3'],
        [0, 'expSortie', 0, 0],
    ]
    return matrice

def tuile4MursV():
    matrice = [
        [0, 0, 1, 0, 1],
        [0, 1, 1, 1, 0],
        [1, 0, 0, 0, 0],
        [0, 1, 1, 0, 0]
    ]
    return matrice

def tuile4MursH():
    matrice = [
        [0, 0, 0, 1],
        [0, 1, 0, 1],
        [1, 0, 0, 1],
        [1, 0, 1, 1],
        [0, 0, 0, 0]
    ]
    return matrice

def tuile5():
    matrice = [
        [1, 1, 'exp4', 1],
        ['exp2', 1, 'sablier', 1],
        ['vortex1', 1, 1, 'exp3'],
        [0, 'expSortie', 1, 0],
    ]
    return matrice

def tuile5MursV():
    matrice = [
        [1, 0, 1, 0, 1],
        [0, 1, 1, 1, 1],
        [1, 0, 0, 0, 0],
        [0, 1, 0, 1, 0]
    ]
    return matrice

def tuile5MursH():
    matrice = [
        [1, 1, 0, 1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0]
    ]
    return matrice

def tuile6():
    matrice = [
        [0, 'o2', 0, 0],
        ['exp3', 1, 1, 0],
        [0, 1, 1, 'exp4'],
        ['vortex1', 'expSortie', 0, 0],
    ]
    return matrice

def tuile6MursV():
    matrice = [
        [0, 1, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0],
        [1, 0, 1, 0, 0]
    ]
    return matrice

def tuile6MursH():
    matrice = [
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [1, 0, 1, 1],
        [1, 0, 0, 0]
    ]
    return matrice

def tuile7():
    matrice = [
        [0, 0, 'o4', 0],
        ['vortex3', 1, 1, 1],
        [0, 0, 0, 'exp1'],
        [0, 'expSortie', 0, 'vortex2'],
    ]
    return matrice

def tuile7MursV():
    matrice = [
        [0, 0, 1, 1, 0],
        [1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0],
        [0, 1, 1, 1, 1]
    ]
    return matrice

def tuile7MursH():
    matrice = [
        [0, 0, 1, 0],
        [1, 1, 0, 1],
        [1, 1, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ]
    return matrice

def tuile8():
    matrice = [
        [1, 1, 1, 1],
        ['exp4', 0, 'vortex2', 1],
        [0, 0, 0, 'exp1'],
        ['o3', 'expSortie', 1, 1],
    ]
    return matrice

def tuile8MursV():
    matrice = [
        [1, 0, 0, 0, 1],
        [0, 1, 1, 1, 1],
        [0, 0, 0, 1, 0],
        [1, 0, 0, 0, 1]
    ]
    return matrice

def tuile8MursH():
    matrice = [
        [1, 1, 1, 1],
        [0, 1, 0, 0],
        [1, 0, 1, 0],
        [1, 1, 1, 0],
        [1, 0, 1, 1]
    ]
    return matrice

def tuile9():
    matrice = [
        [1, 1, 1, 1],
        [1, 0, 'vortex4', 1],
        [1, 1, 0, 'exp2'],
        [0, 'expSortie', 0, 'o1'],
    ]
    return matrice

def tuile9MursV():
    matrice = [
        [1, 0, 0, 0, 1],
        [1, 1, 1, 0, 1],
        [1, 0, 1, 1, 0],
        [0, 1, 1, 1, 1]
    ]
    return matrice

def tuile9MursH():
    matrice = [
        [1, 1, 1, 1],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1]
    ]
    return matrice
