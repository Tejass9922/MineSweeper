import random


row = [-1, -1, -1, 0, 0, 1, 1, 1]
col = [-1, 0, 1, -1, 1, -1, 0, 1]
d = 16
n = 40



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
   
    visited = set()
    remainingCells = set()
    for i in range(len(minMap)):
        for j in range(len(minMap)):
            remainingCells.add(minMap[i][j].location)
    


    

    print("check 1")
    identified_mines = []
    tripped_mines = []
    chosenCellLocation = minMap[xRand][yRand]
    queue = []
    queue.append(chosenCellLocation)
    i = 0
    counter = 0
    while (i < n):
        
        size = len(queue)
        added = False
        
        while (counter < size):
          
            cell = queue.pop()
            print((cell.location, cell.visited))
           
            counter +=1
            visited.add(cell.location)
            remainingCells.remove(cell.location)
            tSize = len(queue)
            if not cell.safe:
                #print("Cell location of tripped mine: ", end = '\t')
                #print(cell.location)
                tripped_mines.append(cell.location)
                cell.visited = -1
                i += 1
                continue

            elif cell.safe:
                cell.clue = getClue(minMap,cell)
                cell.visited = 1
                cell.revealedMines =  revealedMines(minMap, cell)
                hiddenCellsNum = hiddenCells(minMap, cell)
                cell.numHiddenSquares = hiddenCellsNum
                neighbors = getNeighbors(minMap,cell)
                cell.numSafeNeighbors = revealedSafeNeighbors(minMap, cell)
               #  cell.numSafeNeighbors = len(neighbors) - getClue(minMap, cell)

                if (cell.clue- cell.revealedMines == cell.numHiddenSquares):
                    neighbors = getNeighbors(minMap,cell)
                    #print(differenceInClue,cell.numHiddenSquares)
                    print(cell.location)
                    for c in neighbors:
                        print(c.visited)
                        if c.visited == 0 and c.location in remainingCells:
                            c.visited = 2
                            identified_mines.append(c.location)
                            visited.add(c.location)
                            remainingCells.remove(c.location)
                            i += 1

                
                elif ((len(neighbors)- cell.clue) - cell.numSafeNeighbors == cell.numHiddenSquares):
                    for c in neighbors:
                        if c.visited == 0 and c.location in remainingCells:
                            queue.append(c)
                    added = True

            if i >= n:
                break 
        #printTimeSteps(minMap,d)
        #print("--------------------------------------------\n\n")
        #time_step =  input("e")
        if len(visited) == pow(d,2):
            break
        if not added:
            random_location  = random.choice(tuple(remainingCells))
            xRand = random_location[0]
            yRand = random_location[1]
            random_cell = minMap[xRand][yRand]
            queue.append(random_cell)
            '''
            xRand = (random.randint(0,len(minMap)-1))
            yRand = (random.randint(0,len(minMap)-1))
            tlocation = minMap[xRand][yRand]
            while (tlocation.location in visited):
                xRand = (random.randint(0,len(minMap)-1))
                yRand = (random.randint(0,len(minMap)-1))
                tlocation = minMap[xRand][yRand]
            '''
            

            
                   
    printTimeSteps(minMap,d)
    return (identified_mines,tripped_mines)

def solver1t(board, n, d):

    visited = set()
    xRand = (random.randint(0,len(board)-1))
    yRand = (random.randint(0,len(board)-1))
    q = []
    q.append(board[xRand][yRand])
    identified_mines = []
    tripped_mines = []

    total_cells = pow(d,2)
    i = 0
    while (i < n and len(visited) < total_cells):

        size = len(q)
        added = False

        while (size > 0):
            cell = q.pop()
            size -=1
            visited.add(cell.location)
            

            if not cell.safe:
                tripped_mines.append(cell.location)
                cell.visited = -1
                i += 1
                if i >= n:
                    break
                continue
            elif cell.safe:
                cell.visited = 1
                cell.clue = getClue(board, cell)
                cell.revealedMines = revealedMines(board, cell)
                cell.numHiddenSquares = hiddenCells(board,cell)
                cell.numSafeNeighbors = revealedSafeNeighbors(board, cell)
                neighbors = getNeighbors(board, cell)
                
                if cell.clue - cell.revealedMines == cell.numHiddenSquares:
                    for c in neighbors:
                        if c.visited == 0:
                            c.visited = 2
                            visited.add(c.location)
                            identified_mines.append(c.location)
                            i += 1
                elif (len(neighbors) - cell.clue) - cell.numSafeNeighbors == cell.numHiddenSquares:
                    for c in neighbors:
                        if c.visited == 0:
                            c.visited = 1
                            q.append(c)
                    added = True
                
            if i >= n:
                break
        print(cell.location)
        printTimeSteps(board,d)
        input("---------------------------------------------|")
        if (i >= n or len(visited) == pow(d,2)):
            break
        
        if not added:
            
            xRand = random.randint(0,len(board)-1)
            yRand = random.randint(0,len(board)-1)
            random_cell = board[xRand][yRand]
            while random_cell.visited == 1 or random_cell.visited == -1 or random_cell.visited == 2:
                xRand = (random.randint(0,len(board)-1))
                yRand = (random.randint(0,len(board)-1))
                random_cell = board[xRand][yRand] 
            q.append(random_cell)
        
    
    printTimeSteps(board,d)
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



success_rate = []
total_rate = []
for i in range(100):
    minMap = createBoard(n, d)
    (identified, tripped) = solver1(minMap, d, n)
    success_rate.append(len(identified))
    total_rate.append(n)

success = float(float(sum(success_rate))/ float(sum(total_rate)))

print("success rate: ", end = '\t')
print(success)
'''
print("Identified mines : ", end = '\t')
print(identified)
print("Tripped mines : ", end = '\t')
print(tripped)
'''
