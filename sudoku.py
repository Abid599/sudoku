# coding=utf-8
# Abid Rezaiguia 20169670
# Thomaz Oliveira 20154043.
# devoir 2
import PySimpleGUI as sg
import random
import csv
import numpy as np


# import scrape

###################################
# Logique de résolution de Sudoku #
###################################


# Information pertinente: Différence entre "initial state" et "state":
# "initial state" => Les valeurs des éléments text input de la boucle
# principale (donc soit des '1','2',...,'9' ou des '') sous la forme
# d'une liste 2D 9X9

# "state" => l'état de notre solution en contruction composé d'un
# tableau 2D de ints 9x9. Initialement, toutes les cases correspondant
# aux cases vides dans "initialState" (ayant une valeur de '') ont
# une valeur de 0

# Prend initialState et retourne un tableau 2D 9x9 de ints
# où des zéros ont été placés aux cases "vides" ('')
def createInitialGrid(initialState):
    result = []
    for i in initialState:
        arr = []
        for j in i:
            if j == '':
                arr.append(0)
            else:
                arr.append(int(j))

        result.append(arr)
    return result


# Prend un état de la solution, un nombre et retourne si ce nombre
# peut être placé à une certaine position. Au sudoku, on ne peut pas
# placer un même nombre à la même ligne, colonne, ou dans le même bloc
# Une position est un tuple (ligne, colonne)
def isPossible(state, number, position):
    # Valeur dans la même ligne
    for i in range(len(state)):
        if i == position[0]:
            tab = state[i]
            if number in tab:
                return False
    # Valeur dans la même colonne

    for tab in state:
        nombre = tab[position[1]]
        if nombre == number:
            return False

    # Valeur dans le même bloc
    x = position[0]
    y = position[1]

    if x < 3 and y < 3:
        for i in range(3):
            for j in range(3):
                if state[i][j] == number:
                    return False
    elif x < 3 and 3 <= y < 6:
        for i in range(3):
            for j in range(3, 6):
                if state[i][j] == number:
                    return False
    elif x < 3 and 6 <= y < 9:
        for i in range(3):
            for j in range(6, 9):
                if state[i][j] == number:
                    return False

    elif 3 <= x < 6 and y < 3:
        for i in range(3, 6):
            for j in range(3):
                if state[i][j] == number:
                    return False

    elif 3 <= x < 6 and 3 <= y < 6:
        for i in range(3, 6):
            for j in range(3, 6):
                if state[i][j] == number:
                    return False

    elif 3 <= x < 6 and 6 <= y < 9:
        for i in range(3, 6):
            for j in range(6, 9):
                if state[i][j] == number:
                    return False

    elif 6 <= x < 9 and y < 3:
        for i in range(6, 9):
            for j in range(3):
                if state[i][j] == number:
                    return False

    elif 6 <= x < 9 and 3 <= y < 6:
        for i in range(6, 9):
            for j in range(3, 6):
                if state[i][j] == number:
                    return False

    elif 6 <= x < 9 and 6 <= y < 9:
        for i in range(6, 9):
            for j in range(6, 9):
                if state[i][j] == number:
                    return False

    return True


# Retourne la position (ligne, colonne) de la première entrée dans
# intialState qui n'est pas un indice (donc non-vide)
# Retourne None sinon
def findStart(initialState):
    for i in range(len(initialState)):
        for j in range(len(initialState[i])):
            if initialState[i][j] == '':
                return i, j

    return None


# Étant donné la position des indices initiaux, retourne la prochaine
# position qui n'est pas un indice. On traverse le tableau de haut
# en bas, gauche à droite.
def nextCell(initialState, position):
    tab = initialState[position[0]:]
    for i in range(len(tab)):
        for j in range(len(initialState)):
            if i == 0 and j <= position[1]:
                continue
            elif i == 0 and j >= position[1] and tab[i][j] == '':
                return i + position[0], j
            elif i > 0 and tab[i][j] == '':
                return i + position[0], j


# Étant donné la position des indices initiaux, retourne la position
# antérieure qui n'est pas un indice. On traverse le tableau de haut
# en bas, gauche à droite.
def previousCell(initialState, position):
    tab = initialState[:position[0] + 1]
    for i in range(len(tab) - 1, -1, -1):
        for j in range(len(initialState) - 1, -1, -1):
            if i == len(tab) - 1 and j >= position[1]:
                continue
            elif i == len(tab) - 1 and j <= position[1] and tab[i][j] == '':
                return i, j

            elif i < len(tab) - 1 and tab[i][j] == '':
                return i, j


# Retourne si un état initial est valide
# Ne contient pas donc des entrées contradictoires
# i.e. deux chiffres sur la même ligne, colonne, dans le même bloc
# Ainsi qu'un état étant composé de seulement 0-9

# Retourne si un état initial est valide
# Ne contient pas donc des entrées contradictoires
# i.e. deux chiffres sur la même ligne, colonne, dans le même bloc
# Ainsi qu'un état étant composé de seulement 0-9
def isValid(state):
    # pour chaque ligne;
    for tab in state:
        for i in range(len(tab)):
            for j in range(i, len(tab)):
                if j > i and tab[i] == tab[j] and tab[i] != 0:
                    return False

    # pour chaque colonme
    for i in range(len(state)):
        for j in range(len(state)):
            nbr = state[j][i]
            for h in range(j + 1, len(state)):
                nombre = state[h][i]
                if nbr == nombre and nbr != 0 and h > j:
                    return False

        # dans le même bloc.
        for i in range(3):
            for j in range(3):
                nombre = state[i][j]
                for h in range(3):
                    for k in range(3):
                        number = state[h][k]
                        if nombre == number and i != h and k != j and nombre != 0:
                            return False

        for i in range(3):
            for j in range(3, 6):
                nombre = state[i][j]
                for h in range(3):
                    for k in range(3, 6):
                        number = state[h][k]
                        if nombre == number and i != h and k != j and nombre != 0:
                            return False

        for i in range(3):
            for j in range(6, 9):
                nombre = state[i][j]
                for h in range(3):
                    for k in range(6, 9):
                        number = state[h][k]
                        if nombre == number and i != h and k != j and nombre != 0:
                            return False

        for i in range(3, 6):
            for j in range(3):
                nombre = state[i][j]
                for h in range(3, 6):
                    for k in range(3):
                        number = state[h][k]
                        if nombre == number and i != h and k != j and nombre != 0:
                            return False

        for i in range(3, 6):
            for j in range(3, 6):
                nombre = state[i][j]
                for h in range(3, 6):
                    for k in range(3, 6):
                        number = state[h][k]
                        if nombre == number and i != h and k != j and nombre != 0:
                            return False

        for i in range(3, 6):
            for j in range(6, 9):
                nombre = state[i][j]
                for h in range(3, 6):
                    for k in range(6, 9):
                        number = state[h][k]
                        if nombre == number and i != h and k != j and nombre != 0:
                            return False

        for i in range(6, 9):
            for j in range(3):
                nombre = state[i][j]
                for h in range(6, 9):
                    for k in range(3):
                        number = state[h][k]
                        if nombre == number and i != h and k != j and nombre != 0:
                            return False

        for i in range(6, 9):
            for j in range(3, 6):
                nombre = state[i][j]
                for h in range(6, 9):
                    for k in range(3, 6):
                        number = state[h][k]
                        if nombre == number and i != h and k != j and nombre != 0:
                            return False

        for i in range(6, 9):
            for j in range(6, 9):
                nombre = state[i][j]
                for h in range(6, 9):
                    for k in range(6, 9):
                        number = state[h][k]
                        if nombre == number and i != h and k != j and nombre != 0:
                            return False

    return True


# Retourne si un état de recherche est complété
# (Pssst! Ne contender pas de zéros!)
def isCompleted(state):
    for tab in state:
        for nombre in tab:
            if nombre == 0:
                return False
    return True


# Création de la grille initiale à partir du "initialState"
# Implémentation de l'algorithme de "backtracking" jusqu'à
# l'atteinte d'une solution ou de réaliser qu'il n'en existe pas
# Retourne si une solution existe et affiche la solution

def solve(initialState):
    grilleInit = createInitialGrid(initialState)
    firstCell = emptyCell = findStart(initialState)

    while not isCompleted(grilleInit):
        x = emptyCell[0]
        y = emptyCell[1]

        cellValue = grilleInit[x][y]
        for valeur in range(cellValue + 1, 11):

            if valeur < 10 and isPossible(grilleInit, valeur, emptyCell):
                grilleInit[x][y] = valeur
                emptyCell = nextCell(initialState, emptyCell)
                break

            elif valeur == 10:
                grilleInit[x][y] = 0
                if emptyCell == firstCell:
                    return
                emptyCell = previousCell(initialState, emptyCell)

    return grilleInit


########################################################
# Fonctions faisant le pont entre la logique et le GUI #
########################################################

# Affiche '' à chaque InputText
def clearTable():
    # TO DO
    for frame in range(0, 3):
        # ligne dans une matrice
        for column in range(0, 3):
            # element dans une ligne
            for i in range(0, 3):
                for j in range(0, 3):
                    window[(frame, column, i, j)].update('')


# Reçois un tableau de 2 dimensions et affiche son contenu dans la grille d'InputText
def displaySudoku(tab):
    # TO DO
    # prend (x,y) et le transforme en (frame, column, i, j), et l'affiche.

    sudoku = [[[['' for j in range(0, 3)] for i in range(0, 3)] for column in range(0, 3)] for frame in range(0, 3)]
    # print(tab)
    for x in range(1, 10):
        for y in range(1, 10):

            if y <= 3:
                frame = 0

            elif (y >= 4) and (y <= 6):
                frame = 1

            elif y >= 7:
                frame = 2

            if x <= 3:
                column = 0

            elif (x >= 4) and (x <= 6):
                column = 1

            elif x >= 7:
                column = 2

            if y % 3 == 1:
                i = 0

            elif y % 3 == 2:
                i = 1

            elif y % 3 == 0:
                i = 2

            if x % 3 == 1:
                j = 0

            elif x % 3 == 2:
                j = 1

            elif x % 3 == 0:
                j = 2

            sudoku[frame][column][i][j] = tab[y - 1][x - 1]
            window[(frame, column, i, j)].update(sudoku[frame][column][i][j])


def tableau2d(values):
    tab2d = []
    for i in range(9):
        tab = []
        h = 0
        for j in range(9):
            tab.append(values[h])
            values.pop(h)
        tab2d.append(tab)
    return tab2d


# Retourne un tableau 2D à partir du dictionnaire values de la boucle principale
# Les clefs définies pour vos éléments InputText seront utiliè9  sées ici
def getDisplayedSudoku(values):
    # TO DO

    initialState = [['' for x in range(0, 9)] for y in range(0, 9)]
    # si getDisplayedSudoku(values) est utilisée a partir de solve(), values est un dict formés en 9
    # blocs 3x3, il faut donc le transformer en list et le convertir en 2D
    if isinstance(values, dict):
        valuesList = list(values.values())
        values2D = [['' for x in range(0, 9)] for y in range(0, 9)]
        count = 0
        for y in range(0, 9):
            for x in range(0, 9):

                a = valuesList[count]
                values2D[y][x] = a
                count += 1
                if count == 81:
                    break
            if count == 81:
                break

        for bloc in range(0, 9):
            for blocElement in range(0, 9):
                if bloc <= 2:
                    if blocElement <= 2:
                        i = 0
                    elif blocElement >= 3 and blocElement <= 5:
                        i = 1
                    elif blocElement >= 6:
                        i = 2

                elif bloc >= 3 and bloc <= 5:
                    if blocElement <= 2:
                        i = 3
                    elif blocElement >= 3 and blocElement <= 5:
                        i = 4
                    elif blocElement >= 6:
                        i = 5

                elif bloc >= 6:
                    if blocElement <= 2:
                        i = 6
                    elif blocElement >= 3 and blocElement <= 5:
                        i = 7
                    elif blocElement >= 6:
                        i = 8

                if bloc % 3 == 0:
                    if blocElement % 3 == 0:
                        j = 0
                    if blocElement % 3 == 1:
                        j = 1
                    if blocElement % 3 == 2:
                        j = 2

                if bloc % 3 == 1:
                    if blocElement % 3 == 0:
                        j = 3
                    if blocElement % 3 == 1:
                        j = 4
                    if blocElement % 3 == 2:
                        j = 5

                if bloc % 3 == 2:
                    if blocElement % 3 == 0:
                        j = 6
                    if blocElement % 3 == 1:
                        j = 7
                    if blocElement % 3 == 2:
                        j = 8

                initialState[i][j] = values2D[bloc][blocElement]

        return initialState
    else:
        count = 0
        for y in range(0, 9):
            for x in range(0, 9):

                a = values[count]
                initialState[y][x] = a
                count += 1
                if count == 81:
                    return initialState


# Affiche les indices d'un sudoku aléatoire du fichier sudoku.csv
def loadRandomSudoku(data):
    # TO DO
    # taille de data
    tailleData = len(data)

    # choisit un sudoku aléatoirement
    rand = random.randint(0, tailleData - 1)
    print("rand: " + str(rand))
    values = data[rand]
    print("values: " + str(values))

    initialState = getDisplayedSudoku(values)
    # print(initialState)
    return initialState


data = []
vide = [['', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', ''],
        ['', '', '', '', '', '', '', '', '']]

with open('sudoku.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

sg.theme('DarkAmber')

layout = []

# Ajout de 81 InputText au layout. Ne pas utiliser une boucle ici
# sera sévèrement pénalisé. Attention d'également bien choisir vos "key"s

layout += [
    [[[sg.Frame('', [
        [sg.Input("", size=(4, 50), key=(frame, column, i, j), pad=(0, 0, 0, 0)) for j in
         range(0, 3)] for i in range(0, 3)]) for column in range(0, 3)] for frame in range(0, 3)]],
    [sg.Button('Load'),
     sg.Button('Solve'),
     sg.Button('Clear')]]

# Create the Window
window = sg.Window('Sudoku Solver', layout, element_justification='c')
initialState = vide
# Event Loop to process "events" and get the "values" of the inputs
while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    elif event == 'Clear':
        clearTable()
        initialState = vide
    elif event == 'Load':
        initialState = loadRandomSudoku(data)
        print(initialState)
        # Insère les valeurs de initialGrid dans le layout GUI.
        displaySudoku(initialState)

    elif event == 'Solve':
        if initialState == vide:
            displaySudoku(solve(vide))
        print(solve(initialState))
        displaySudoku(solve(initialState))

window.close()

#########
# TESTS #
#########

# Ajouter les tests nécessaires pour chaque fonction
# Voici quelques exemples (qui sont loin d'être suffisants):

assert createInitialGrid([['', '', '', '5', '', '9', '', '', '2'],
                          ['', '3', '5', '', '', '2', '', '9', '5'],
                          ['', '9', '6', '', '', '', '4', '', ''],
                          ['', '', '', '1', '2', '6', '9', '', ''],
                          ['4', '', '3', '5', '', '9', '1', '', '6'],
                          ['', '', '9', '7', '3', '4', '', '1', ''],
                          ['', '', '5', '', '', '', '4', '6', ''],
                          ['', '', '', '9', '', '', '2', '1', ''],
                          ['1', '', '', '8', '', '2', '', '', '']]) == [[0, 0, 0, 5, 0, 9, 0, 0, 2],
                                                                        [0, 3, 5, 0, 0, 2, 0, 9, 5],
                                                                        [0, 9, 6, 0, 0, 0, 4, 0, 0],
                                                                        [0, 0, 0, 1, 2, 6, 9, 0, 0],
                                                                        [4, 0, 3, 5, 0, 9, 1, 0, 6],
                                                                        [0, 0, 9, 7, 3, 4, 0, 1, 0],
                                                                        [0, 0, 5, 0, 0, 0, 4, 6, 0],
                                                                        [0, 0, 0, 9, 0, 0, 2, 1, 0],
                                                                        [1, 0, 0, 8, 0, 2, 0, 0, 0]]

assert isPossible([[0, 0, 0, 0, 8, 5, 1, 0, 9],
                   [0, 0, 0, 7, 3, 0, 8, 0, 4],
                   [0, 8, 0, 0, 0, 0, 0, 0, 6],
                   [6, 5, 0, 0, 0, 1, 0, 0, 3],
                   [0, 0, 2, 0, 0, 0, 1, 0, 0],
                   [4, 0, 0, 9, 0, 0, 0, 6, 2],
                   [5, 0, 0, 0, 0, 0, 0, 3, 0],
                   [6, 0, 3, 0, 5, 7, 0, 0, 0],
                   [8, 0, 9, 6, 1, 0, 0, 0, 0]], 9, (2, 4)) == True

assert isPossible([[0, 0, 0, 0, 8, 5, 1, 0, 9],
                   [0, 0, 0, 7, 3, 0, 8, 0, 4],
                   [0, 8, 0, 0, 0, 0, 0, 0, 6],
                   [6, 5, 0, 0, 0, 1, 0, 0, 3],
                   [0, 0, 2, 0, 0, 0, 1, 0, 0],
                   [4, 0, 0, 9, 0, 0, 0, 6, 2],
                   [5, 0, 0, 0, 0, 0, 0, 3, 0],
                   [6, 0, 3, 0, 5, 7, 0, 0, 0],
                   [8, 0, 9, 6, 1, 0, 0, 0, 0]], 6, (2, 0)) == False

assert isPossible([[4, 0, 0, 0, 0, 0, 0, 0, 5],
                   [0, 0, 9, 4, 0, 2, 8, 0, 0],
                   [0, 6, 0, 0, 5, 0, 0, 9, 0],
                   [0, 3, 0, 0, 8, 0, 0, 2, 0],
                   [0, 0, 2, 5, 0, 1, 3, 0, 0],
                   [0, 9, 0, 0, 4, 0, 0, 7, 0],
                   [0, 1, 0, 0, 6, 0, 0, 5, 0],
                   [0, 0, 8, 1, 0, 5, 9, 0, 0],
                   [5, 0, 0, 0, 0, 0, 0, 0, 7]], 9, (6, 0)) == True

assert isPossible([[4, 0, 0, 0, 0, 0, 0, 0, 5],
                   [0, 0, 9, 4, 0, 2, 8, 0, 0],
                   [0, 6, 0, 0, 5, 0, 0, 9, 0],
                   [0, 3, 0, 0, 8, 0, 0, 2, 0],
                   [0, 0, 2, 5, 0, 1, 3, 0, 0],
                   [0, 9, 0, 0, 4, 0, 0, 7, 0],
                   [0, 1, 0, 0, 6, 0, 0, 5, 0],
                   [0, 0, 8, 1, 0, 5, 9, 0, 0],
                   [5, 0, 0, 0, 0, 0, 0, 0, 7]], 9, (7, 0)) == False

assert nextCell([['', '', '', '', '8', '5', '1', '', '9'],
                 ['', '', '', '7', '3', '', '8', '', '4'],
                 ['', '8', '', '', '', '', '', '', '6'],
                 ['6', '5', '', '', '', '1', '', '', '3'],
                 ['', '', '2', '', '', '', '1', '', ''],
                 ['4', '', '', '9', '', '', '', '6', '2'],
                 ['5', '', '', '', '', '', '', '3', ''],
                 ['6', '', '3', '', '5', '7', '', '', ''],
                 ['8', '', '9', '6', '1', '', '', '', '']], (1, 3)) == (1, 5)

assert nextCell([['9', '', '', '', '2', '', '', '', '7'],
                 ['', '6', '', '7', '', '8', '', '9', '5'],
                 ['', '', '', '', '', '6', '8', '4', ''],
                 ['8', '2', '', '', '6', '', '', '5', '3'],
                 ['', '', '7', '', '', '', '4', '', ''],
                 ['4', '3', '', '', '7', '', '', '1', '8'],
                 ['', '8', '9', '1', '', '', '', '', ''],
                 ['6', '7', '', '4', '', '9', '', '3', ''],
                 ['1', '', '', '', '3', '', '', '', '9']], (2, 5)) == (2, 8)

assert nextCell([['9', '', '', '', '2', '', '', '', '7'],
                 ['', '6', '', '7', '', '8', '', '9', '5'],
                 ['', '', '', '', '', '6', '8', '4', ''],
                 ['8', '2', '', '', '6', '', '', '5', '3'],
                 ['', '', '7', '', '', '', '4', '', ''],
                 ['4', '3', '', '', '7', '', '', '1', '8'],
                 ['', '8', '9', '1', '', '', '', '', ''],
                 ['6', '7', '', '4', '', '9', '', '3', ''],
                 ['1', '', '', '', '3', '', '', '', '9']], (2, 4)) == (2, 8)

assert previousCell([['9', '', '', '', '2', '', '', '', '7'],
                     ['', '6', '', '7', '', '8', '', '9', '5'],
                     ['', '', '', '', '', '6', '8', '4', ''],
                     ['8', '2', '', '', '6', '', '', '5', '3'],
                     ['', '', '7', '', '', '', '4', '', ''],
                     ['4', '3', '', '', '7', '', '', '1', '8'],
                     ['', '8', '9', '1', '', '', '', '', ''],
                     ['6', '7', '', '4', '', '9', '', '3', ''],
                     ['1', '', '', '', '3', '', '', '', '9']], (2, 4)) == (2, 3)

assert previousCell([['', '', '', '', '8', '5', '1', '', '9'],
                     ['', '', '', '7', '3', '', '8', '', '4'],
                     ['', '8', '', '', '', '', '', '', '6'],
                     ['6', '5', '', '', '', '1', '', '', '3'],
                     ['', '', '2', '', '', '', '1', '', ''],
                     ['4', '', '', '9', '', '', '', '6', '2'],
                     ['5', '', '', '', '', '', '', '3', ''],
                     ['6', '', '3', '', '5', '7', '', '', ''],
                     ['8', '', '9', '6', '1', '', '', '', '']], (4, 0)) == (3, 7)

assert previousCell([['', '', '', '', '8', '5', '1', '', '9'],
                     ['', '', '', '7', '3', '', '8', '', '4'],
                     ['', '8', '', '', '', '', '', '', '6'],
                     ['6', '5', '', '', '', '1', '', '', '3'],
                     ['', '', '2', '', '', '', '1', '', ''],
                     ['4', '', '', '9', '', '', '', '6', '2'],
                     ['5', '', '', '', '', '', '', '3', ''],
                     ['6', '', '3', '', '5', '7', '', '', ''],
                     ['8', '', '9', '6', '1', '', '', '', '']], (8, 5)) == (8, 1)

assert isValid([[4, 0, 9, 0, 0, 0, 0, 0, 5],
                [0, 0, 9, 4, 0, 2, 8, 0, 0],
                [0, 6, 0, 0, 5, 0, 0, 9, 0],
                [0, 3, 0, 0, 8, 0, 0, 2, 0],
                [0, 0, 2, 5, 0, 1, 3, 0, 0],
                [0, 9, 0, 0, 4, 0, 0, 7, 0],
                [0, 1, 0, 0, 6, 0, 0, 5, 0],
                [0, 0, 8, 1, 0, 5, 9, 0, 0],
                [5, 0, 0, 0, 0, 0, 0, 0, 7]]) == False

assert isValid([[4, 0, 0, 0, 0, 0, 0, 0, 5],
                [0, 0, 9, 4, 0, 2, 8, 0, 0],
                [0, 6, 0, 0, 5, 0, 0, 9, 0],
                [0, 3, 0, 0, 8, 0, 0, 2, 0],
                [0, 0, 2, 5, 0, 1, 3, 0, 0],
                [0, 9, 0, 0, 4, 0, 0, 7, 0],
                [0, 1, 0, 0, 6, 0, 0, 5, 0],
                [0, 0, 8, 1, 0, 5, 9, 0, 0],
                [5, 0, 0, 0, 0, 0, 0, 0, 712312301203]]) == False

assert isValid([[9, 0, 0, 0, 4, 0, 0, 0, 8],
                [5, 0, 1, 7, 0, 8, 4, 0, 0],
                [0, 8, 3, 9, 0, 0, 0, 0, 0],
                [7, 0, 4, 0, 1, 0, 9, 0, 3],
                [0, 1, 0, 0, 0, 0, 0, 7, 0],
                [3, 0, 6, 0, 5, 0, 2, 0, 4],
                [0, 0, 0, 0, 0, 5, 7, 3, 0],
                [0, 0, 5, 1, 0, 3, 8, 0, 2],
                [8, 0, 0, 0, 6, 0, 0, 0, 1]]) == True

assert isCompleted([[4, 4, 4, 4, 4, 4, 4, 4, 5],
                    [4, 4, 9, 4, 4, 4, 8, 4, 4],
                    [5, 6, 5, 5, 5, 5, 5, 9, 5],
                    [7, 3, 7, 7, 8, 7, 7, 2, 7],
                    [8, 8, 2, 5, 8, 1, 3, 8, 8],
                    [1, 9, 1, 1, 4, 1, 1, 7, 1],
                    [2, 1, 2, 2, 6, 2, 2, 5, 2],
                    [3, 3, 8, 1, 3, 5, 9, 3, 3],
                    [5, 5, 5, 5, 5, 5, 5, 5, 0]]) == False

assert isCompleted([[1, 8, 3, 4, 5, 9, 2, 7, 6],
                    [6, 4, 5, 7, 3, 2, 1, 8, 9],
                    [2, 7, 9, 8, 6, 1, 4, 5, 3],
                    [4, 2, 7, 9, 1, 8, 6, 3, 5],
                    [3, 6, 8, 5, 7, 4, 9, 2, 1],
                    [5, 9, 1, 6, 2, 3, 7, 4, 8],
                    [7, 1, 2, 3, 8, 6, 5, 9, 4],
                    [9, 3, 6, 2, 4, 5, 8, 1, 7],
                    [8, 5, 4, 1, 9, 7, 3, 6, 2]]) == True

assert solve([['1', '', '3', '4', '5', '9', '', '', ''],
              ['6', '', '5', '', '', '', '', '', ''],
              ['', '', '9', '8', '', '1', '', '5', ''],
              ['', '2', '7', '9', '1', '8', '', '', ''],
              ['3', '', '', '', '', '', '', '', '1'],
              ['', '', '', '6', '2', '3', '7', '4', ''],
              ['', '1', '', '3', '', '6', '5', '', ''],
              ['', '', '', '', '', '', '8', '', '7'],
              ['', '', '', '1', '9', '7', '3', '', '2']]) == [[1, 8, 3, 4, 5, 9, 2, 7, 6],
                                                              [6, 4, 5, 7, 3, 2, 1, 8, 9],
                                                              [2, 7, 9, 8, 6, 1, 4, 5, 3],
                                                              [4, 2, 7, 9, 1, 8, 6, 3, 5],
                                                              [3, 6, 8, 5, 7, 4, 9, 2, 1],
                                                              [5, 9, 1, 6, 2, 3, 7, 4, 8],
                                                              [7, 1, 2, 3, 8, 6, 5, 9, 4],
                                                              [9, 3, 6, 2, 4, 5, 8, 1, 7],
                                                              [8, 5, 4, 1, 9, 7, 3, 6, 2]]

assert findStart([['1', '', '3', '4', '5', '9', '', '', ''],
                  ['6', '', '5', '', '', '', '', '', ''],
                  ['', '', '9', '8', '', '1', '', '5', ''],
                  ['', '2', '7', '9', '1', '8', '', '', ''],
                  ['3', '', '', '', '', '', '', '', '1'],
                  ['', '', '', '6', '2', '3', '7', '4', ''],
                  ['', '1', '', '3', '', '6', '5', '', ''],
                  ['', '', '', '', '', '', '8', '', '7'],
                  ['', '', '', '1', '9', '7', '3', '', '2']]) == (0, 1)

assert solve([['3', '', '', '2', '', '8', '7', '', ''],
              ['8', '', '5', '', '1', '', '2', '', ''],
              ['', '2', '1', '', '', '5', '6', '4', '8'],
              ['2', '7', '', '', '', '', '', '', ''],
              ['', '', '', '6', '', '3', '', '', ''],
              ['', '', '', '', '', '', '', '7', '4'],
              ['5', '1', '2', '8', '', '', '4', '3', ''],
              ['', '', '7', '', '5', '', '1', '', '6'],
              ['', '', '8', '9', '', '1', '', '', '7']]) == [[3, 9, 6, 2, 4, 8, 7, 1, 5],
                                                             [8, 4, 5, 7, 1, 6, 2, 9, 3],
                                                             [7, 2, 1, 3, 9, 5, 6, 4, 8],
                                                             [2, 7, 9, 5, 8, 4, 3, 6, 1],
                                                             [1, 8, 4, 6, 7, 3, 9, 5, 2],
                                                             [6, 5, 3, 1, 2, 9, 8, 7, 4],
                                                             [5, 1, 2, 8, 6, 7, 4, 3, 9],
                                                             [9, 3, 7, 4, 5, 2, 1, 8, 6],
                                                             [4, 6, 8, 9, 3, 1, 5, 2, 7]]
