import random


row = [-1, -1, -1, 0, 0, 1, 1, 1]
col = [-1, 0, 1, -1, 1, -1, 0, 1]
d = 5
n = 5



class Cell:
    def __init__(self, safe, revealedMines, clue, numSafeNeighbors, numHiddenSquares, visited, location):
        self.safe = safe
        self.revealedMines = revealedMines
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

        if (minMap[x][y].returnSafe()):
            minMap[x][y].safe = False
            numMines = numMines - 1

    for i in range(len(minMap)):
        for j in range(len(minMap)):
            print(minMap[i][j].safe, end = '\t')
        print('\n')
    return minMap

def printboard(minMap, d):
    for i in range(d):
        for j in range(d):
            if(minMap[i][j].safe == True):
                print("_\t", end=' ')
            else:
                print("*\t", end=' ')
        print('\n')

def printTimeSteps(board, d):
    for i in range(d):
        for j in range(d):
            if(board[i][j].visited == 1):
                print(board[i][j].clue, end='\t')
            elif (board[i][j].visited == 0):
                print("-", end='\t')
            elif (board[i][j].visited == -1):
                print("TM", end = '\t')
            elif(board[i][j].visited == 2):
                print("IM", end = '\t')

        print('\n')

def createBoard(n, d):
    minMap = [[Cell(True, None, None, None, None, 0, (i, j)) for j in range(d)] for i in range(d)]
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
            if (board[x][y].visited == -1 or board[x][y].visited == 2):
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



def solver(minMap, d, n):
    identified_mines = []
    tripped_mines = []
    visited = set()
    inferenced_cells = set()
    i = 0
    while (i < n):
        
        revealed = False
        
        for row in range(len(minMap)):
            for col in range(len(minMap)):
                cell = minMap[row][col] 
                
                #inference if statements 
                if cell.visited == 1 and not cell.location in inferenced_cells:
                   
                    cell.clue = getClue(minMap,cell)
                    cell.revealedMines =  revealedMines(minMap, cell)
                    cell.numHiddenSquares =  hiddenCells(minMap, cell)
                    neighbors = getNeighbors(minMap,cell)
                    cell.numSafeNeighbors = revealedSafeNeighbors(minMap, cell)
                    
                    if (cell.clue - cell.revealedMines == cell.numHiddenSquares):
                        print((cell.location, cell.clue,cell.revealedMines, cell.numHiddenSquares, cell.numSafeNeighbors))
                        print("all mines")
                        neighbors = getNeighbors(minMap,cell)
                        
                        for c in neighbors:
                          
                            if c.visited == 0:
                                c.visited = 2
                                identified_mines.append(c.location)
                                #inferenced_cells.add(c.location)
                                i += 1
                        inferenced_cells.add(cell.location)
                        revealed = True

                        #added = True
                        print("random i val check: ", end = ' ')
                        print(i)

                    elif ((len(neighbors)- cell.clue) - cell.numSafeNeighbors == cell.numHiddenSquares):
                        print("all safe")
                        for c in neighbors:
                            print((c.location, c.visited, minMap[c.location[0]][c.location[1]].location))
                            if c.visited == 0 :
                                c.visited = 1
                                #inferenced_cells.add(c.location)
                        inferenced_cells.add(cell.location)
                        revealed = True

                
                       
               
        if i >= n:
            break
        if not revealed:
            print("random cell adding")
            #print("not added")
            remainingCells = set()
            for r in range(len(minMap)):
                for c in range(len(minMap)):
                    if  minMap[r][c].visited == 0:
                        remainingCells.add(minMap[r][c].location)

            if len(remainingCells) > 0:
                random_location  = random.choice(tuple(remainingCells))
                xRand = random_location[0]
                yRand = random_location[1]
                random_cell = minMap[xRand][yRand]
                if random_cell.safe:
                    minMap[xRand][yRand].visited = 1
                    #visited.add(minMap[xRand][yRand].visited)
                    #inferenced_cells.add(minMap[xRand][yRand].visited)
                else:
                    minMap[xRand][yRand].visited = -1
                    tripped_mines.append(random_cell.location)
                    inferenced_cells.add(minMap[xRand][yRand].location)
                    i += 1
            else:
                break

        
        #input("---------------------------------------------------------------------------->")
        printTimeSteps(minMap,d)
    

    return (identified_mines,tripped_mines)     



'''
# -- Advanced Agent--
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

board = createBoard(n,d)

'''
success_rate = []
total_rate = []
scores = []
counter = 0
for i in range(100):
    minMap = createBoard(n_mines, dim)
    (identified, tripped) = solver(minMap, dim, n_mines)
   
    s1 = set(identified)
    s2  = set(tripped)
    if (len(s1.intersection(s2)) != 0):
        counter += 1
    print("----------------------------->")
    print("Identified: ", end = ' ')
    print(identified)
    print("Tripped: ", end = ' ')
    print(tripped)
    success_rate.append(len(identified))
    print("----------------------------->")
    total_rate.append(n_mines)
for i in range(len(minMap)):
    for j in range(len(minMap)):
        print(minMap[i][j].visited, end = '\t')

    print('\n')

success = ((sum(success_rate)))
total =  (sum(total_rate))
print(counter)
rate = float(float(success)/ float(total))
print("success rate: ", end = '\t')
print(rate)
''
'''
'''
print("Identified mines : ", end = '\t')
print(identified)
print("Tripped mines : ", end = '\t')
print(tripped)
'''





    
