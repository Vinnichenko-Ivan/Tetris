import pygame
from enum import Enum
import random
from random import randint

DEBUG = False
# --------------------------------------------------------------------------------------------------------------
WIDTH = 300
HEIGHT = 450
FPS = 60
GAMEHARDER = 60

CELLCOUNTX = 10
CELLCOUNTY = 20
CELLSIZEXPX = 20
CELLSIZEXPY = 20
GAMEFILDWIDTH = CELLSIZEXPX *  CELLCOUNTX
GAMEFILDHEIGHT = CELLSIZEXPY *  CELLCOUNTY

# --------------------------------------------------------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (156, 39, 176)
INDIGO = (63, 81, 181)
BLUE = (33, 150, 243)
GREEN = (76, 175, 80)
YELLOW = (255, 235, 59)
ORANGE = (255, 152, 0)
GREY = (158, 158, 158)
RED = (100, 0, 0)

class MoveType(Enum):
    Down = 1
    Left = 2
    Right = 3
    Сlockwise = 4
    Сounterclockwise = 5
    Fast = 6
    Nothing = 7

class Turn(Enum):
    Down = 1
    Left = 2
    Right = 3
    Up = 4


TypeFigure = {1 : 'l', 2 : 'o', 3 : 'j', 4 : 't', 5 : 'z', 6 : 's', 7 : 'i'}

class Block:
    existence = False
    stay = False
    color = (0, 0, 255)

class Figure:
    type = 'l'
    blocks = []
    color = (0, 0, 255)
    turn = Turn.Up
    def __init__(self, inType):
        self.type = inType
        self.blocks = [[0, 0], [0, 0], [0, 0], [0, 0]]
        if(self.type == 'i'):
            self.blocks[0][0] = 4
            self.blocks[1][0] = 5
            self.blocks[2][0] = 6
            self.blocks[3][0] = 7
            self.color = BLUE
        if(self.type == 't'):
            self.blocks[0][0] = 4
            self.blocks[1][0] = 5
            self.blocks[2][0] = 6
            self.blocks[3][0] = 5
            self.blocks[3][1] = 1
            self.color = PURPLE
        if(self.type == 'j'):
            self.blocks[0][0] = 4
            self.blocks[1][0] = 5
            self.blocks[2][0] = 6
            self.blocks[3][0] = 4
            self.blocks[3][1] = 1
            self.color = (33, 200, 243)
        if(self.type == 'l'):
            self.blocks[0][0] = 4
            self.blocks[1][0] = 5
            self.blocks[2][0] = 6
            self.blocks[3][0] = 6
            self.blocks[3][1] = 1
            self.color = ORANGE
        if(self.type == 'o'):
            self.blocks[0][0] = 5
            self.blocks[1][0] = 5
            self.blocks[2][0] = 6
            self.blocks[3][0] = 6
            self.blocks[3][1] = 1
            self.blocks[0][1] = 1
            self.color = YELLOW
        if(self.type == 's'):
            self.blocks[0][0] = 7
            self.blocks[1][0] = 5
            self.blocks[2][0] = 6
            self.blocks[3][0] = 6
            self.blocks[3][1] = 1
            self.blocks[0][1] = 1
            self.color = GREEN
        if(self.type == 'z'):
            self.blocks[0][0] = 5
            self.blocks[1][0] = 5
            self.blocks[2][0] = 6
            self.blocks[3][0] = 4
            self.blocks[3][1] = 1
            self.blocks[0][1] = 1
            self.color = RED

class Fild:
    figure = Figure('z')
    realFild = [[]]
    result = 0
    def __init__(self):
        for x in range(0, 10):
            self.realFild.append([])
            for y in range(0, 20):
                self.realFild[x].append(Block())

    def testLine(self):
        counter = 0
        delLine = []
        for y in range(0, 20):
            flag = True
            for x in range(0, 10):
                if(self.realFild[x][y].existence == False):
                    flag = False
            if(flag):
                counter += 1
                delLine.append(y)
        for y in delLine:
            for x in range(0, 10):
                self.realFild[x][y].existence = False
        for yDel in delLine:
            for y in range(yDel, 0, -1):
                for x in range(0, 10):
                    self.realFild[x][y].existence = self.realFild[x][y - 1].existence
                    self.realFild[x][y].color = self.realFild[x][y - 1].color


    def reset(self):
        self.realFild.clear()
        for x in range(0, 10):
            self.realFild.append([])
            for y in range(0, 20):
                self.realFild[x].append(Block())
        self.result = 0

    def newFigure(self):
        self.figure = Figure(TypeFigure[randint(1, 7)])
        flag = False
        for n in self.figure.blocks:
            if (self.realFild[n[0]][n[1]].existence):
                flag = True
        if(flag):
            self.reset()

    def step(self,typeMove = MoveType.Down):
        try:
            if(typeMove == MoveType.Down):
                flag = True
                for n in self.figure.blocks:
                    if(n[1] == 19):
                        flag = False
                    elif(self.realFild[n[0]][n[1] + 1].existence):
                        flag = False
                if(flag):
                    self.figure.blocks[0][1] += 1
                    self.figure.blocks[1][1] += 1
                    self.figure.blocks[2][1] += 1
                    self.figure.blocks[3][1] += 1
                else:
                    self.realFild[self.figure.blocks[0][0]][self.figure.blocks[0][1]].existence = True
                    self.realFild[self.figure.blocks[1][0]][self.figure.blocks[1][1]].existence = True
                    self.realFild[self.figure.blocks[2][0]][self.figure.blocks[2][1]].existence = True
                    self.realFild[self.figure.blocks[3][0]][self.figure.blocks[3][1]].existence = True
                    if DEBUG == False:
                        self.realFild[self.figure.blocks[0][0]][self.figure.blocks[0][1]].color = self.figure.color
                        self.realFild[self.figure.blocks[1][0]][self.figure.blocks[1][1]].color = self.figure.color
                        self.realFild[self.figure.blocks[2][0]][self.figure.blocks[2][1]].color = self.figure.color
                        self.realFild[self.figure.blocks[3][0]][self.figure.blocks[3][1]].color = self.figure.color
                    self.newFigure()
                    self.testLine()
            if (typeMove == MoveType.Left):
                flag = True
                for n in self.figure.blocks:
                    if (n[0] == 0):
                        flag = False
                    elif (self.realFild[n[0] - 1][n[1]].existence):
                        flag = False
                if (flag):
                    self.figure.blocks[0][0] -= 1
                    self.figure.blocks[1][0] -= 1
                    self.figure.blocks[2][0] -= 1
                    self.figure.blocks[3][0] -= 1
            if (typeMove == MoveType.Right):
                flag = True
                for n in self.figure.blocks:
                    if (n[0] == 9):
                        flag = False
                    elif (self.realFild[n[0] + 1][n[1]].existence):
                        flag = False
                if (flag):
                    self.figure.blocks[0][0] += 1
                    self.figure.blocks[1][0] += 1
                    self.figure.blocks[2][0] += 1
                    self.figure.blocks[3][0] += 1
            if (typeMove == MoveType.Сlockwise):
                if(self.figure.type == 'i'):
                    if(self.figure.turn == Turn.Up):
                        flag = True
                        if(False):
                            flag = False
                        elif(self.realFild[self.figure.blocks[0][0] + 2][self.figure.blocks[0][1] - 2].existence):
                            flag = False
                        elif(self.realFild[self.figure.blocks[1][0] + 1][self.figure.blocks[1][1] - 1].existence):
                            flag = False
                        elif(self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        if(flag):
                            self.figure.blocks[0][0] += 2
                            self.figure.blocks[0][1] -= 2
                            self.figure.blocks[1][0] += 1
                            self.figure.blocks[1][1] -= 1
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Right
                    elif(self.figure.turn == Turn.Right):
                        flag = True
                        if(False):
                            flag = False
                        elif(self.realFild[self.figure.blocks[0][0] + 2][self.figure.blocks[0][1] + 2].existence):
                            flag = False
                        elif(self.realFild[self.figure.blocks[1][0] + 1][self.figure.blocks[1][1] + 1].existence):
                            flag = False
                        elif(self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        if(flag):
                            self.figure.blocks[0][0] += 2
                            self.figure.blocks[0][1] += 2
                            self.figure.blocks[1][0] += 1
                            self.figure.blocks[1][1] += 1
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Down
                    elif(self.figure.turn == Turn.Down):
                        flag = True
                        if(False):
                            flag = False
                        elif(self.realFild[self.figure.blocks[0][0] - 2][self.figure.blocks[0][1] + 2].existence):
                            flag = False
                        elif(self.realFild[self.figure.blocks[1][0] - 1][self.figure.blocks[1][1] + 1].existence):
                            flag = False
                        elif(self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        if(flag):
                            self.figure.blocks[0][0] -= 2
                            self.figure.blocks[0][1] += 2
                            self.figure.blocks[1][0] -= 1
                            self.figure.blocks[1][1] += 1
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Left
                    elif(self.figure.turn == Turn.Left):
                        flag = True
                        if(False):
                            flag = False
                        elif(self.realFild[self.figure.blocks[0][0] - 2][self.figure.blocks[0][1] - 2].existence):
                            flag = False
                        elif(self.realFild[self.figure.blocks[1][0] - 1][self.figure.blocks[1][1] - 1].existence):
                            flag = False
                        elif(self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        if(flag):
                            self.figure.blocks[0][0] -= 2
                            self.figure.blocks[0][1] -= 2
                            self.figure.blocks[1][0] -= 1
                            self.figure.blocks[1][1] -= 1
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Up
                elif (self.figure.type == 'l'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 2][self.figure.blocks[3][1] + 0].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] -= 2
                            self.figure.blocks[3][1] += 0
                            self.figure.turn = Turn.Right
                    elif (self.figure.turn == Turn.Right):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] - 2].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 0][self.figure.blocks[3][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] -= 2
                            self.figure.blocks[3][0] -= 0
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Down
                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 2][self.figure.blocks[3][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] -= 0
                            self.figure.blocks[3][0] += 2
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Left
                    elif (self.figure.turn == Turn.Left):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 0][self.figure.blocks[3][1] + 2].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] += 0
                            self.figure.blocks[3][1] += 2
                            self.figure.turn = Turn.Up
                elif (self.figure.type == 'j'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 0][self.figure.blocks[3][1] - 2].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] -= 0
                            self.figure.blocks[3][1] -= 2
                            self.figure.turn = Turn.Right
                    elif (self.figure.turn == Turn.Right):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 2][self.figure.blocks[3][1] - 0].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] -= 1
                            self.figure.blocks[3][0] += 2
                            self.figure.blocks[3][1] -= 0
                            self.figure.turn = Turn.Down
                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 0][self.figure.blocks[3][1] + 2].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] -= 1
                            self.figure.blocks[3][0] += 0
                            self.figure.blocks[3][1] += 2
                            self.figure.turn = Turn.Left
                    elif (self.figure.turn == Turn.Left):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 2][self.figure.blocks[3][1] + 0].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] -= 2
                            self.figure.blocks[3][1] += 0
                            self.figure.turn = Turn.Up
                elif (self.figure.type == 't'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[3][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Right
                    elif (self.figure.turn == Turn.Right):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[3][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] -= 1
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Down
                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][1] + 1][self.figure.blocks[2][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[3][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] -= 1
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Left
                    elif (self.figure.turn == Turn.Left):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[3][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Up
                elif (self.figure.type == 's'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 0][self.figure.blocks[0][1] - 2].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 1][self.figure.blocks[1][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 0][self.figure.blocks[2][1] + 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[3][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 0
                            self.figure.blocks[0][1] -= 2
                            self.figure.blocks[1][0] += 1
                            self.figure.blocks[1][1] += 1
                            self.figure.blocks[2][0] -= 0
                            self.figure.blocks[2][1] += 0
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Down
                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 0][self.figure.blocks[0][1] + 2].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] - 1][self.figure.blocks[1][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 0][self.figure.blocks[2][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[3][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 0
                            self.figure.blocks[0][1] += 2
                            self.figure.blocks[1][0] -= 1
                            self.figure.blocks[1][1] -= 1
                            self.figure.blocks[2][0] -= 0
                            self.figure.blocks[2][1] += 0
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Up
                elif (self.figure.type == 'z'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 0][self.figure.blocks[0][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] - 1][self.figure.blocks[1][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 2][self.figure.blocks[2][1] + 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[3][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 0
                            self.figure.blocks[0][1] -= 0
                            self.figure.blocks[1][0] -= 1
                            self.figure.blocks[1][1] += 1
                            self.figure.blocks[2][0] -= 2
                            self.figure.blocks[2][1] += 0
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Down

                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 0][self.figure.blocks[0][1] + 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 1][self.figure.blocks[1][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 2][self.figure.blocks[2][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[3][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 0
                            self.figure.blocks[0][1] -= 0
                            self.figure.blocks[1][0] += 1
                            self.figure.blocks[1][1] -= 1
                            self.figure.blocks[2][0] += 2
                            self.figure.blocks[2][1] -= 0
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Up
            if (typeMove == MoveType.Сounterclockwise):
                if(self.figure.type == 'i'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 2][self.figure.blocks[0][1] + 2].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 1][self.figure.blocks[1][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 2
                            self.figure.blocks[0][1] += 2
                            self.figure.blocks[1][0] += 1
                            self.figure.blocks[1][1] += 1
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Left
                    elif (self.figure.turn == Turn.Right):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 2][self.figure.blocks[0][1] + 2].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] - 1][self.figure.blocks[1][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 2
                            self.figure.blocks[0][1] += 2
                            self.figure.blocks[1][0] -= 1
                            self.figure.blocks[1][1] += 1
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Up
                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 2][self.figure.blocks[0][1] - 2].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] - 1][self.figure.blocks[1][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 2
                            self.figure.blocks[0][1] -= 2
                            self.figure.blocks[1][0] -= 1
                            self.figure.blocks[1][1] -= 1
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Right
                    elif (self.figure.turn == Turn.Left):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 2][self.figure.blocks[0][1] - 2].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 1][self.figure.blocks[1][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 2
                            self.figure.blocks[0][1] -= 2
                            self.figure.blocks[1][0] += 1
                            self.figure.blocks[1][1] -= 1
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Down
                elif (self.figure.type == 'l'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 0][self.figure.blocks[3][1] - 2].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] -= 1
                            self.figure.blocks[3][0] -= 0
                            self.figure.blocks[3][1] -= 2
                            self.figure.turn = Turn.Left
                    elif (self.figure.turn == Turn.Left):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 2][self.figure.blocks[3][1] - 0].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] -= 2
                            self.figure.blocks[3][1] -= 0
                            self.figure.turn = Turn.Down
                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 0][self.figure.blocks[3][1] + 2].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] += 0
                            self.figure.blocks[3][1] += 2
                            self.figure.turn = Turn.Right
                    elif (self.figure.turn == Turn.Right):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 2][self.figure.blocks[3][1] + 0].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] -= 1
                            self.figure.blocks[3][0] += 2
                            self.figure.blocks[3][1] += 0
                            self.figure.turn = Turn.Up
                elif (self.figure.type == 'j'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 2][self.figure.blocks[3][1] + 0].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] -= 1
                            self.figure.blocks[3][0] += 2
                            self.figure.blocks[3][1] -= 0
                            self.figure.turn = Turn.Left
                    elif (self.figure.turn == Turn.Left):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 0][self.figure.blocks[3][1] - 2].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] -= 0
                            self.figure.blocks[3][1] -= 2
                            self.figure.turn = Turn.Down
                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 2][self.figure.blocks[3][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] -= 2
                            self.figure.blocks[3][1] += 0
                            self.figure.turn = Turn.Right
                    elif (self.figure.turn == Turn.Right):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 0][self.figure.blocks[3][1] + 2].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] -= 1
                            self.figure.blocks[3][0] += 0
                            self.figure.blocks[3][1] += 2
                            self.figure.turn = Turn.Up
                elif (self.figure.type == 't'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[3][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] -= 1
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Left
                    elif (self.figure.turn == Turn.Left):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[3][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] -= 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Down
                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[3][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] -= 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] += 1
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Right
                    elif (self.figure.turn == Turn.Right):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 1][self.figure.blocks[0][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 0][self.figure.blocks[1][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 1][self.figure.blocks[2][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[3][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] -= 1
                            self.figure.blocks[0][1] += 1
                            self.figure.blocks[1][0] += 0
                            self.figure.blocks[1][1] -= 0
                            self.figure.blocks[2][0] += 1
                            self.figure.blocks[2][1] -= 1
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Up
                elif (self.figure.type == 's'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 0][self.figure.blocks[0][1] - 2].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 1][self.figure.blocks[1][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 0][self.figure.blocks[2][1] + 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[3][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 0
                            self.figure.blocks[0][1] -= 2
                            self.figure.blocks[1][0] += 1
                            self.figure.blocks[1][1] += 1
                            self.figure.blocks[2][0] -= 0
                            self.figure.blocks[2][1] += 0
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Down
                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 0][self.figure.blocks[0][1] + 2].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] - 1][self.figure.blocks[1][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 0][self.figure.blocks[2][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[3][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 0
                            self.figure.blocks[0][1] += 2
                            self.figure.blocks[1][0] -= 1
                            self.figure.blocks[1][1] -= 1
                            self.figure.blocks[2][0] -= 0
                            self.figure.blocks[2][1] += 0
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Up
                elif (self.figure.type == 'z'):
                    if (self.figure.turn == Turn.Up):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] + 0][self.figure.blocks[0][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] - 1][self.figure.blocks[1][1] + 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] - 2][self.figure.blocks[2][1] + 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] + 1][self.figure.blocks[3][1] + 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 0
                            self.figure.blocks[0][1] -= 0
                            self.figure.blocks[1][0] -= 1
                            self.figure.blocks[1][1] += 1
                            self.figure.blocks[2][0] -= 2
                            self.figure.blocks[2][1] += 0
                            self.figure.blocks[3][0] += 1
                            self.figure.blocks[3][1] += 1
                            self.figure.turn = Turn.Down

                    elif (self.figure.turn == Turn.Down):
                        flag = True
                        if (False):
                            flag = False
                        elif (self.realFild[self.figure.blocks[0][0] - 0][self.figure.blocks[0][1] + 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[1][0] + 1][self.figure.blocks[1][1] - 1].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[2][0] + 2][self.figure.blocks[2][1] - 0].existence):
                            flag = False
                        elif (self.realFild[self.figure.blocks[3][0] - 1][self.figure.blocks[3][1] - 1].existence):
                            flag = False
                        if (flag):
                            self.figure.blocks[0][0] += 0
                            self.figure.blocks[0][1] -= 0
                            self.figure.blocks[1][0] += 1
                            self.figure.blocks[1][1] -= 1
                            self.figure.blocks[2][0] += 2
                            self.figure.blocks[2][1] -= 0
                            self.figure.blocks[3][0] -= 1
                            self.figure.blocks[3][1] -= 1
                            self.figure.turn = Turn.Up
            if (typeMove == MoveType.Fast):
                stayFlag = True
                while stayFlag:
                    flag = True
                    for n in self.figure.blocks:
                        if(n[1] == 19):
                            flag = False
                        elif(self.realFild[n[0]][n[1] + 1].existence):
                            flag = False
                    if(flag):
                        self.figure.blocks[0][1] += 1
                        self.figure.blocks[1][1] += 1
                        self.figure.blocks[2][1] += 1
                        self.figure.blocks[3][1] += 1
                    else:
                        self.realFild[self.figure.blocks[0][0]][self.figure.blocks[0][1]].existence = True
                        self.realFild[self.figure.blocks[1][0]][self.figure.blocks[1][1]].existence = True
                        self.realFild[self.figure.blocks[2][0]][self.figure.blocks[2][1]].existence = True
                        self.realFild[self.figure.blocks[3][0]][self.figure.blocks[3][1]].existence = True
                        if DEBUG == False:
                            self.realFild[self.figure.blocks[0][0]][self.figure.blocks[0][1]].color = self.figure.color
                            self.realFild[self.figure.blocks[1][0]][self.figure.blocks[1][1]].color = self.figure.color
                            self.realFild[self.figure.blocks[2][0]][self.figure.blocks[2][1]].color = self.figure.color
                            self.realFild[self.figure.blocks[3][0]][self.figure.blocks[3][1]].color = self.figure.color
                        self.newFigure()
                        self.testLine()
                        stayFlag = False

        except:
            print("mass error")



def drawFild(fild):
    for x in range(0, 10):
        for y in range(0, 20):
            if(fild.realFild[x][y].existence):
                pygame.draw.rect(screen, fild.realFild[x][y].color, (10 + x * CELLSIZEXPX, 10 + y * CELLSIZEXPY, CELLSIZEXPX - 2, CELLSIZEXPY - 2))
    for n in fild.figure.blocks:
        pygame.draw.rect(screen, fild.figure.color, (10 + n[0] * CELLSIZEXPX, 10 + n[1] * CELLSIZEXPY, CELLSIZEXPX - 2, CELLSIZEXPY - 2))

def drawDevice(screen):
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREY, (0, 0, WIDTH, 10))
    pygame.draw.rect(screen, GREY, (0, 0, 10, HEIGHT))
    pygame.draw.rect(screen, GREY, (0, HEIGHT - 10, WIDTH, 10))
    pygame.draw.rect(screen, GREY, (WIDTH - 10, 0, 10, HEIGHT))
    for x in range(CELLSIZEXPX + 10, GAMEFILDWIDTH + 10, CELLSIZEXPX):
        pygame.draw.line(screen, GREY, (x, 0), (x, GAMEFILDHEIGHT + 10))
    for y in range(CELLSIZEXPY + 10, GAMEFILDHEIGHT + 10, CELLSIZEXPY):
        pygame.draw.line(screen, GREY, (0, y), (GAMEFILDWIDTH + 10, y))
    pygame.draw.rect(screen, GREY, (0, GAMEFILDHEIGHT + 10, WIDTH, HEIGHT))
    pygame.draw.rect(screen, GREY, (GAMEFILDWIDTH + 10, 0, WIDTH, HEIGHT))

# --------------------------------------------------------------------------------------------------------------
pygame.init()
#pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
running = True

counterS = 0
fild = Fild()

# --------------------------------------------------------------------------------------------------------------

while running:
    clock.tick(FPS)
    counterS += 1
    if(counterS % GAMEHARDER == 0):
        counterS = 0
        fild.step( MoveType.Down)
    moveType = MoveType.Nothing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moveType = MoveType.Left
            elif event.key == pygame.K_RIGHT:
                moveType = MoveType.Right
            elif event.key == pygame.K_UP:
                moveType = MoveType.Down
            elif event.key == pygame.K_DOWN:
                moveType = MoveType.Fast
            elif event.key == pygame.key.key_code("a"):
                moveType = MoveType.Left
            elif event.key == pygame.key.key_code("d"):
                moveType = MoveType.Right
            elif event.key == pygame.key.key_code("e"):
                moveType = MoveType.Сlockwise
            elif event.key == pygame.key.key_code("q"):
                moveType = MoveType.Сounterclockwise
            elif event.key == pygame.key.key_code("s"):
                moveType = MoveType.Fast
            elif event.key == pygame.K_u:
                FPS += 5
            elif event.key == pygame.K_j:
                FPS -= 5

    fild.step(moveType)
    drawDevice(screen)
    drawFild(fild)
    pygame.display.flip()

pygame.quit()