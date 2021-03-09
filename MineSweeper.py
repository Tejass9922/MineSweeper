import random


row = [-1, -1, -1, 0, 0, 1, 1, 1]
col = [-1, 0, 1, -1, 1, -1, 0, 1]
d = 5
n = 10
d = 5
n = 10

class Cell:
    def __init__(self, safe, numMinesInden, clue, numSafeNeighbors, numHiddenSquares, visited, location):
        self.safe = safe
        self.numMinesInden = numMinesInden
        self.clue = clue
        self.numSafeNeighbors = numSafeNeighbors
        self.numHiddenSquares = numHiddenSquares
        self.visited = visited
        self.location = location
    def __eq__(self, other):
        return (self.location == other.location)

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
    minMap = [[Cell(True, None, None, None, None, 0, (j, i)) for j in range(d)] for i in range(d)]
    minMap = populateMines(minMap, n, d)
    printboard(minMap, d)
    return minMap


def getClue(board, cell):
    clue = 0
    n = len(board)
    for i in range(8):
        x = row[i] + cell.location[0]
        y = col[i]  + cell.location[1]
        if x >= 0 and x < n and y >=0 and y < n:
            print(x, y)
            if (board[x][y].safe == False):
                clue += 1
    return clue

def getNeighbors(board, cell):
    neighbors  = []
    n = len(board)
    for i in range(8):
        x = row[i] + cell.location[0]
        y = col[i]  + cell.location[1]
        if x >= 0 and x < n and y >=0 and y < n:
            neighbors.append(board[x][y])
    return neighbors

def hiddenCells(board, cell):
    hiddenCellsNums = 0
    n = len(board)
    for i in range(8):
        x = row[i] + cell.location[0]
        y = col[i]  + cell.location[1]
        if x >= 0 and x < n and y >=0 and y < n:
            if (board[x][y].visited == 0):
                hiddenCellsNums += 1
    return hiddenCellsNums

def revealedMines(board, cell):
    revealedMines = 0
    n = len(board)
    for i in range(8):
        x = row[i] + cell.location[0]
        y = col[i]  + cell.location[1]
        if x >= 0 and x < n and y >=0 and y < n:
            if (board[x][y].visited == -1):
                revealedMines += 1
    return revealedMines

def revealedSafeNeighbors(board, cell):
    revealedSafeNeighbors = 0
    n = len(board)
    for i in range(8):
        x = row[i] + cell.location[0]
        y = col[i]  + cell.location[1]
        if x >= 0 and x < n and y >=0 and y < n:
            if (board[x][y].visited == 1):
                revealedSafeNeighbors += 1
    return revealedSafeNeighbors

def solver1(minMap, d, n):
    xRand = (random.randint(0,len(minMap)-1))
    yRand = (random.randint(0,len(minMap)-1))
   
    remainingCells = set()
    for i in range(len(minMap)):
        for j in range(len(minMap)):
            remainingCells.add(minMap[i][j].location)


    identified_mines = []
    tripped_mines = []
    chosenCellLocation = minMap[xRand][yRand]
    queue = [chosenCellLocation]
    i = 0
    while (i < n):
        
        size = len(queue)
        while (len(queue) > 0):
            
            cell = queue.pop()
            remainingCells.remove(cell.location)
            tSize = len(queue)
            if not cell.safe:
                tripped_mines.append(cell.location)
                cell.visited = -1
                i += 1
                continue

            elif cell.safe:
                cell.visited = 1
                differenceInClue = getClue(minMap, cell) - revealedMines(minMap, cell)
                hiddenCellsNum = hiddenCells(minMap, cell)
                cell.numHiddenSquares = hiddenCellsNum
                neighbors = getNeighbors(minMap,cell)
                cell.numSafeNeighbors = len(neighbors) - getClue(minMap, cell)

            if (differenceInClue == cell.numHiddenSquares):
                neighbors = getNeighbors(minMap,cell)
                for c in neighbors:
                    c.visited = -1
                    identified_mines.append(c.location)
                    i += 1

            cell.numSafeNeighbors = revealedSafeNeighbors(minMap, cell)
            if ((cell.numSafeNeighbors - cell.numRevealedNeighbors) == cell.numHiddenSquares):
                for c in neighbors:
                    queue.append(c)
            if len(queue) == tSize:
                xRand = (random.randint(0,len(minMap)-1))
                yRand = (random.randint(0,len(minMap)-1))
                tlocation = minMap[xRand][yRand]
                while (tlocation.visted == 1 or tlocation.visited == 0 or tlocation.location in remainingCells):
                    xRand = (random.randint(0,len(minMap)-1))
                    yRand = (random.randint(0,len(minMap)-1))
                    tlocation = minMap[xRand][yRand]
                queue.append(tlocation)

            if i >= n:
                break
                   

    return (identified_mines,tripped_mines)

'''
def kbEquation(minMap, cell):
    (neighbors, clue) = getNeighborsandClue(minMap, cell)
    cell.clue = clue
    KB[cell] = neighbors
    """
    retrie neighbor locations
    retrieve clue value
    create dictionary element
        key: Object containing location and clue 
        value: set of neighbors (objects containing locations)"""
    return 

def solver2(minMap, d, n):
    switch = 0 #used for breaking out of loop when you find a 0 (safe) value
    numMines = n
    
    while (numMines > 0):
        switch = 0
       
        while (switch != 1): #while you have not found a new spot to uncover 
            
            for keyA in KB:
                for keyB in KB:
                    if (not keyA == keyB):
                        keySetA = KB[keyA] #gets the set of neighbors from the equation
                        keySetB = KB[keyB] #gets the set of neighbors from the equation

                        if (len(keySetB) >= len(keySetA) and keyB.clue > keyA.clue): #checks to make sure B has a larger sets size and clue value
                            newSet = keySetB.difference(keySetB) #gets the difference in sets
                            newClue = (keyB.clue - keyA.clue) #gets the difference in clue values

                        #if clue is 0 
                        if (newClue == 0):
                            for i in newSet:
                                i.safe = True
                        
                        #if clue is 1
                        if ((newClue/len(newSet) == 1):
                            for i in newSet:
                                i.safe = False 
                        #if clue > 1

                        """
                        check to see if the length of KEYSetB is greater than keySetA and that KeyB clue is greater than KeyA clue
                        if it is
                            subtract keySetA from keySetB 
                                *check length of subtraction to see if there was any difference
                                create a new set (equation value)
                            subtract KeyA clue from KeyB clue
                                create a new clue (index value)
                            create a new equation
                            check if the clue == 0 or 1
                                modify Map to reflect that
                                if clue == 1
                                    switch = 1
                                        ***Implement:
                                            chooses that value as the next location
                                            creates a equation
                                            
                                else 
                                    numMines -= 1
                        if not 
                            contiue over (**Don't want negative numbers)
                        """
                
    

'''


minMap = createBoard(n, d)
(identified, tripped) = solver1(minMap, 5, 10)
print(identified)
print(tripped)
