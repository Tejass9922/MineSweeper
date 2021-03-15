import random


row = [-1, -1, -1, 0, 0, 1, 1, 1]
col = [-1, 0, 1, -1, 1, -1, 0, 1]
d = 9
n = 10



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
    minMap = createBoard(n, d)
    (identified, tripped) = solver(minMap, d, n)
   
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
    total_rate.append(n)
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


'''


    
'''
'''
--Tejas Pseudocode----

def heuristic_assignments(KB,board,eq,clue):
    assignment_set = set()
    --Based on length of eq, return possible assignments for variables if any

    if len(eq) == 1: 
        variable = NULL
            for e in eq:
                variable = e
                break
        if clue == 1:
            variable.assignment = 1
        else:
            variable.assignment = 0

        assignment_set.add(variable)

    elif len(eq) == 2:
        negative_counter = 0
        for e in eq:
            negative_counter += 1 if e.negative else 0

        if clue == 0:
           if negative_counter == 0 or negative_counter == 2:
               for e in eq:
                   e.assignment = 0
                   assignment_set.add(e)
            if negative_counter == 1:
                for e in eq:
                    e.assignment = 1
                    assignment_set.add(e)
        
        if clue == 1:
            if negative_counter == 1:
                for e in eq:
                    if e.negative:
                        e.assignmnet = 0
                    else:
                        e.assignment = 1
                    
                    assignment_set.add(e)
        
        if clue == 2:
            for e in eq:
                e.assignment = 1
                assignment_set.add(e)

    return assignmnet_set




def solver2(KB, board, d, n):

    iidentified_mines = []
    tripped_mines = []
    visited = set()
    inferenced_cells = set()
  while (mines_found < n):
        revealed = False
        assignment set = [] # set of Assignment tuples that can grow over time in the iteration. Tuple that holds : (cell location, assignment (0 or 1)) ) 0 is safe and 1 is mine
        
        #INFERENCE STEP
        for keyA in KB:
            for keyB in KB:
                if keyA == keyB:
                    continue
                if KB.get(keyA).intersect(KB.get(keyA)):
                    #Trim KB to make sure it only holds unique equations
                    KB.remove(keyB)
                    continue
                --check subtraction of 2 sets: (2 conditions, intersect and len or subtraction)
                    #Note make an object where the set elements are comparable 
                    eq1 = KB.get(keyA)
                    eq2 = KB.get(keyB)
                    if len(eq1.intersect(eq2)) > 0:
                        #Check which clue is bigger
                       
                   
                         #Create Temp set of variables before assignmnet of positive or negative signs
                        eqt = eq1.union(eq2)- eq2.intersection(eq1) 
                        eq3 = set()
                        sent_clue = abs(keyA - keyB)
                        if keyA[1] > keyB[1]:
                            for e in eqt:
                                if e in eq2:
                                    #Create Variable class : (location,sign(True = +, False = -), assignment)
                                    eq3.add(Variable(e.location,False,None))
                                elif e in eq1:
                                    eq3.add(Variable(e.location,True,None))
                        else:
                             for e in eqt:
                                if e in eq1:
                                    #Create Variable class : (location,sign(True = +, False = -), assignment)
                                    eq3.add(Variable(e.location,False,None))
                                elif e in eq2:
                                    eq3.add(Variable(e.location,True,None))

                        if len(eq3) <= min{len(eq1), len(eq2)}: 
                            --check len:
                                case 1: len = 1
                                        - reveal first and then create assignment set? or flip?? idk the benefit (most likely going to add to assignment set and then reveal in second loop)
                                case 2: len = 2
                                        - call heuristic function to deal with that to get an assignemnt set
                                            assignment_set = heuristic(KB,board,eq3,sent_clue)
                                            - if assignment set len == 0
                                                - create new key and add eq to KB
                                case 3: len > 2:
                                        - call heuristic to try to get an assignment set
                                         assignment_set = heuristic(KB,board,eq3,sent_clue)

                                        -- if assignment_set comes back empty, add eq right away to the KB

                        

        
        #REDUCE KNOWLEDGE BASE
       
        #Stores assignment set for final stage of decision making
        assignment_set_copy = assignment_set

        #loop until our assignment set is empty, this will avoid any case where an assignment reduction casues a new assignment. In this case we can just add the new one back to our assignment set
        if len(assignment_set) > 0:
            revealed = true
        while len(assignment_set) > 0
            for keyC in KB:
                eq = KB.get(keyC)
                #2 options, use intersect or just nest the loops. Probably going with nesting because we are dealing with 2 different types of objects??
                    #--update: utilize same object for assignment sets and KB equation objects. easier that way

                for assignment in assignment_set:
                    if assignment in eq:
                        if assignment.assignmnet == 1:
                            keyC.clue -= 1
                            identified_mines.append(assignment.location)
                            mines_found  += 1

                        eq.remove(assignment) #position of this statement and the above subject to change
                        
                        if len(eq) == 0:
                            KB.remove(keyC)
                        if len(eq) == 1 or 2:
                            in_set_already = False

                            #Prevents double assignmnets 
                            for e in eq:
                                if e in assignmnet_set:
                                    in_set_already = True
                                    break

                            if not in_set_already:
                                call heuristic
                                new_set = return value from heuristic
                                assignment_set.add(new_set)
                                assignment_set_copy.add(new_set)

                    
                    

        #DECISION STEP: REVEAL ASSIGNMENTS

        clue_counter = len(KB)
        for assignment in assignment_set_copy:
        if assignment.safe:
            location = assignment.location 

            x = location[0]
            y = location[1]
            board[x][y].visited = 1
            clue_temp = getClue(location)
            clue = clue_temp - revealedMines(location)
            hiddenNeighbors = getHiddenNeighbors(location)
            
            
            #This will be objects. Could take up multiple lines of code to make them into objects though.
            #Will be hashed based on location
            eq = set(hiddenNeighbors) 

            clue_counter += 1
            KB.add((clue_counter,clue), eq)


    #RANDOM ASSIGNMENT

    if not revealed:
            
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
                ---#Create equation for the Cell---
                    #Includes creating new instance of Variable object (see line 443 for example)
                    #and adding it to the KB by incrementing the clue counter
            else:
                minMap[xRand][yRand].visited = -1
                tripped_mines.append(random_cell.location)
                ---#Update KB---
                mines_found += 1
        else:
            break

    printTimeSteps(board,d)

    return (identified_mines,tripped_mines)

          
--end Tejas PsuedoCode


        
                
            
                

        
                                


'''
