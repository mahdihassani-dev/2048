import random

import colorama
import numpy
import os
from pynput import keyboard
from colorama import Fore
from colorama import Style

m = numpy.zeros((4, 4), dtype=int)
matrix_selection = [0] * 4
moved = [0]


def decimalTo4BaseNum(i):
    result = []
    if (i < 4):
        result.append(0)
        result.append(i)
    else:
        while i > 0:
            result.insert(0, i % 4)
            i = i // 4
    return result


def proportion_8020():
    proportion = random.randint(1, 10)
    if proportion >= 8:
        return 4
    else:
        return 2


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def isLoser():
    for i in range(4):
        for j in range(4):
            if m[i][j] == 0:
                return False

    for i in range(4):
        for j in range(0, 3, 1):
            if m[i][j] == m[i][j + 1]:
                return False

    for i in range(4):
        for j in range(0, 3, 1):
            if m[j][i] == m[j + 1][i]:
                return False

    return True


def addRandomNumInEachMove():
    if not any(0 in sublist for sublist in m):
        return

    x1 = random.randint(0, 3)
    x2 = random.randint(0, 3)

    while m[x1][x2] != 0:
        x1 = random.randint(0, 3)
        x2 = random.randint(0, 3)

    m[x1][x2] = proportion_8020()


def movement(par):
    clear_screen()

    # shift based on arrowKey
    for i in range(4):
        Shift(par, i)

    # add new number if some movement happenedd
    if moved[0] == 1:
        addRandomNumInEachMove()
        moved[0] = 0

    # set new game table
    setGameTable(m)

    # check if losed
    if isLoser():
        print("you losed")


# 1- first initialize 2 random in cells
def setInitialRandomNumbers():
    # each item has a unique number from 1-16
    item_numberings = []
    for i in range(0, 15, 1):
        item_numberings.append(i)

    # get a random number from matrix
    a = random.choice(item_numberings)
    # remove that number from matrix to choose another one
    item_numberings.remove(a)
    b = random.choice(item_numberings)

    # to get the position in 2D matrix
    x1 = decimalTo4BaseNum(a)[0]
    y1 = decimalTo4BaseNum(a)[1]
    x2 = decimalTo4BaseNum(b)[0]
    y2 = decimalTo4BaseNum(b)[1]

    # get 2 or 4 with ratio of 80% / 20%
    m[x1][y1] = proportion_8020()
    m[x2][y2] = proportion_8020()


# 2- set the table in the first and in each move
def setGameTable(m):
    colorama.init()

    print("+-------+-------+-------+-------+")
    for i in range(4):
        for j in range(4):
            number = m[i][j]
            if 0 <= number <= 9:
                match (number):
                    case 0:
                        print(f"|   {number}   ", end="")
                    case 2:
                        print(f"|   {Fore.RED}{number}{Style.RESET_ALL}   ", end="")
                    case 4:
                        print(f"|   {Fore.BLUE}{number}{Style.RESET_ALL}   ", end="")
                    case 8:
                        print(f"|   {Fore.GREEN}{number}{Style.RESET_ALL}   ", end="")
            elif 10 <= number <= 99:
                match (number):
                    case 16:
                        print(f"|   {Fore.LIGHTBLACK_EX}{number}{Style.RESET_ALL}  ", end="")
                    case 32:
                        print(f"|   {Fore.YELLOW}{number}{Style.RESET_ALL}  ", end="")
                    case 64:
                        print(f"|   {Fore.LIGHTGREEN_EX}{number}{Style.RESET_ALL}  ", end="")
            elif 100 <= number <= 999:
                match (number):
                    case 128:
                        print(f"|  {Fore.LIGHTRED_EX}{number}{Style.RESET_ALL}  ", end="")
                    case 256:
                        print(f"|  {Fore.MAGENTA}{number}{Style.RESET_ALL}  ", end="")
                    case 512:
                        print(f"|  {Fore.LIGHTBLUE_EX}{number}{Style.RESET_ALL}  ", end="")
            elif 1000 <= number <= 9999:
                print(f"|  {number} ", end="")
            elif 10000 <= number <= 99999:
                print(f"| {number} ", end="")
            elif 100000 <= number <= 999999:
                print(f"| {number}", end="")
            if j == 3:
                print("|")
                if i < 3:
                    print("+-------+-------+-------+-------+")
                else:
                    print("+-------+-------+-------+-------+")


# 3- detect arrow keys pressed
def on_press(key):
    if key == keyboard.Key.up:
        movement(0)
    if key == keyboard.Key.down:
        movement(2)
    if key == keyboard.Key.left:
        movement(3)
    if key == keyboard.Key.right:
        movement(1)
    if key == keyboard.Key.esc:
        listener.stop()


# 4- get rows and columns from matrix
def ParseTheMatrix(par, num):  # Change line and column to a, b, c and d.

    match par:
        case 0:
            matrix_selection[0] = m[0][num]
            matrix_selection[1] = m[1][num]
            matrix_selection[2] = m[2][num]
            matrix_selection[3] = m[3][num]
        case 1:
            matrix_selection[0] = m[num][3]
            matrix_selection[1] = m[num][2]
            matrix_selection[2] = m[num][1]
            matrix_selection[3] = m[num][0]
        case 2:
            matrix_selection[0] = m[3][num]
            matrix_selection[1] = m[2][num]
            matrix_selection[2] = m[1][num]
            matrix_selection[3] = m[0][num]
        case 3:
            matrix_selection[0] = m[num][0]
            matrix_selection[1] = m[num][1]
            matrix_selection[2] = m[num][2]
            matrix_selection[3] = m[num][3]

    return matrix_selection


# 5- shift rows and columns based on arrowKey
def Shift(par, num):  # Shift a, b, c and d.

    ParseTheMatrix(par, num)

    a = matrix_selection[0]
    b = matrix_selection[1]
    c = matrix_selection[2]
    d = matrix_selection[3]

    for i in range(3):

        if a == 0:
            a = b
            b = c
            c = d
            d = 0
            moved[0] = 1

        if b == 0:
            b = c
            c = d
            d = 0
            moved[0] = 1

        if c == 0:
            c = d
            d = 0
            moved[0] = 1

    Sum(par, num, a, b, c, d)


# 6- sum cells if it is possible
def Sum(par, num, a, b, c, d):  # For sum a, b, c and d.

    if a == b and a != 0:
        a += b
        b = c
        c = d
        d = 0
        moved[0] = 1
    if b == c and b != 0:
        b += c
        c = d
        d = 0
        moved[0] = 1

    if c == d and c != 0:
        c += d
        d = 0
        moved[0] = 1

    PassToMatrix(par, num, a, b, c, d)


# 7- pass new columns and rows to the matrix
def PassToMatrix(par, num, a, b, c, d):  # This function save our a, b, c and d at list m.

    match par:
        case 0:
            m[0][num] = a
            m[1][num] = b
            m[2][num] = c
            m[3][num] = d
        case 1:
            m[num][3] = a
            m[num][2] = b
            m[num][1] = c
            m[num][0] = d
        case 2:
            m[3][num] = a
            m[2][num] = b
            m[1][num] = c
            m[0][num] = d
        case 3:
            m[num][0] = a
            m[num][1] = b
            m[num][2] = c
            m[num][3] = d


setInitialRandomNumbers()
setGameTable(m)

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
