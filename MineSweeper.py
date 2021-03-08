import random

class Cell:

    def __init__(self, safe, numMinesInden, clue, numSafeNeighbors, numHiddenSquares):
        self.safe = safe
        self.numMinesInden = numMinesInden
        self.clue = clue
        self.numSafeNeighbors = numSafeNeighbors
        self.numHiddenSquares = numHiddenSquares
    def returnSafe(self):
        return self.safe
    """def __repr__(self):
        if self.safe == True:
            return ("Not a Mine")
        elif self.safe == False:
            return ("Cell is a Mine")
        else:
            return ("Cell not initialized")"""

def populateMines(minMap, n, d):
    testList = list(range(0, d))
    numMines = n
    while(numMines > 0):
        x = random.choice(testList)
        y = random.choice(testList)
        #print(x)
        #print(y)
        if (minMap[x][y].returnSafe()):
            minMap[x][y].safe = False
            numMines = numMines - 1
    return minMap

def printboard(minMap, d):
    for i in range(d):
        for j in range(d):
            if(minMap[i][j].safe == True):
                print("_\t", end=' ')
            else:
                print("*\t", end=' ')
        print('\n')

def createBoard(n, d):
    minMap = [[Cell(True, None, None, None, None) for j in range(d)] for i in range(d)]
    minMap = populateMines(minMap, n, d)
    printboard(minMap, d)

def makeInferences(minMap, )
    cluesDictionary = {}
    

d = 5
n = 10

createBoard(n, d)
