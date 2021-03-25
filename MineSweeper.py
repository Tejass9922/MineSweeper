import random
#from sympy import * 
import numpy as np
from copy import deepcopy

row = [-1, -1, -1, 0, 0, 1, 1, 1]
col = [-1, 0, 1, -1, 1, -1, 0, 1]
d = 6
n = 9

#[26, 51, 77, 102, 128, 154, 179, 205, 230]
class Variable:
    def __init__(self,location,isNegative,assignment):
        self.location = location
        self.isNegative = isNegative
        self.assignment = assignment

    def __eq__(self,other):
        return self.location == other.location
    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return str(self.location)

class Key:
    def __init__(self,location,clue_count,clue):
        self.location = location
        self.clue = clue
        self.clue_count = clue_count

    def __eq__(self, other):
        return self.clue == other.clue and self.clue_count == other.clue_count and self.location == other.location

    def __hash__(self):
        return self.clue_count

    def __repr__(self):
        return str((self.location,self.clue,self.clue_count))
     
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
            print(minMap[i][j].safe, end= '\t')
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

def getClueV2(board,location):
    clue = 0
    n = len(board)
    for i in range(8):
        x = row[i] + location[0]
        y = col[i] + location[1]
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

def getHiddenNeighbors(board,location):
    n = len(board)
    hiddenNeighbors = []
    for i in range(8):
        x = row[i] + location[0]
        y = col[i] + location[1]
        if x >= 0 and x < n and y >=0 and y < n and board[x][y].visited == 0:
            hiddenNeighbors.append((x,y))

    return hiddenNeighbors


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

def revealedMinesV2(board, location):
    revealedMines = 0
    n = len(board)
    for i in range(8):
        x = row[i] +  location[0]
        y = col[i]  + location[1]
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


#BASIC INFERENCE ALGORITHM
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

def basic_solver_play_by_play(minMap, d, n):
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

        
        input("---------------------------------------------------------------------------->")
        printTimeSteps(minMap,d)
    

    return (identified_mines,tripped_mines)



def subset_solver(KB,board,clue_counter,inferenced_cells):
    flagged_mines = []
    threat_flag = []
    safe_neighbors = []
    flagged_mines = []
    anything_assigned = False
    for keyA in KB:
        for keyB in KB:
            if keyA == keyB:
                continue

            eq1 = KB[keyA]
            eq2 = KB[keyB]

            keyA_clue = keyA.clue
            keyB_clue = keyB.clue
            if eq1==eq2 and not (keyA in threat_flag):
                threat_flag.append(keyA)
                continue


            if eq1.issubset(eq2):
                eq3 = eq2.difference(eq1)
                eq3_len = len(eq3)
                clue_val_diff = abs(keyA_clue - keyB_clue)
                if clue_val_diff == 0:
                    print("---STRONG INFERENCE MADE FOR SAFE NEIGHBORS---")
                   
                    print("eq1: " + str(eq1))
                    print("eq2: " + str(eq2))
                    print("eq3: " + str(eq3))
                    print("clue_difference: " + str(clue_val_diff))
                    for var in eq3:
                        location = var.location
                        x = location[0]
                        y = location[1]
                        board[x][y].visited = 1
                        var.assignment = 0
                        anything_assigned = True
                        safe_neighbors.append(var)
                    
                elif clue_val_diff == len(eq3):
                    print("---STRONG INFERENCE MADE FOR POTENTIAL MINES---")
                    print("eq1: " + str(eq1))
                    print("eq2: " + str(eq2))
                    print("eq3: " + str(eq3))
                    print("clue_difference: " + str(clue_val_diff))
                    for var in eq3:
                        location = var.location
                        x = location[0]
                        y = location[1]
                        board[x][y].visited = 2
                        var.assignment = 1
                        anything_assigned= True
                        flagged_mines.append(var)
    
    #FLAG MINES
    
    for xf in flagged_mines:
        for k in KB:
            eq = KB[k]
            if xf in eq:
                k.clue -= 1
     
    for xd in flagged_mines:
        for k in KB:
            eq = KB[k]
            eq.discard(xd)
    
    
    #REDUCE SAFE NEIGHBORS
    

    for yn in safe_neighbors:
        for k in KB:
            eq = KB[k]
            eq.discard(yn)

    #CHECK FOR EMPTY KEYS

    #ADD VARIABLES
    
   
    for s in safe_neighbors:
        
        if s.assignment == 0:
            location = s.location 

            x = location[0]
            y = location[1]
            board[x][y].visited = 1
            
            clue_temp = getClueV2(board,location)
            clue = clue_temp - revealedMinesV2(board,location)
            board[x][y].clue = clue
            hiddenNeighbors = getHiddenNeighbors(board,location)
            
            
            #This will be objects. Could take up multiple lines of code to make them into objects though.
            #Will be hashed based on location
            #Create new Variable objects for each of the hidden neighbors based on location
            variable_set = []
            for neighbor in hiddenNeighbors:
                v = Variable(neighbor,False,None)
                variable_set.append(v)

            eq = set(variable_set) 

            clue_counter += 1
            add_key = Key(location,clue_counter,clue)
            KB[add_key] = eq


    for keyA in KB:
        for keyB in KB:
            eq1 = KB[keyA]
            eq2 = KB[keyB]
            if keyA == keyB:
                continue
            if eq1 == eq2 and not (keyA) in threat_flag:
                threat_flag.append(keyA)


    for t in threat_flag:
        KB.pop(t)

        

    return (KB,board,flagged_mines,anything_assigned)

#TODO- random_assignment / adding to KB
def rebuild_KB(KB,board,inferenced_cells):
    KB = {}
    clue_counter = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j].visited == 1 and not board[i][j].location in inferenced_cells:
                location = (i,j)
                clue_temp = getClueV2(board,location)
                clue = clue_temp - revealedMinesV2(board,location)
                board[i][j].clue = clue_temp
                hiddenNeighbors = getHiddenNeighbors(board,location)
                
                
                #This will be objects. Could take up multiple lines of code to make them into objects though.
                #Will be hashed based on location
                #Create new Variable objects for each of the hidden neighbors based on location
                variable_set = []
                for neighbor in hiddenNeighbors:
                    v = Variable(neighbor,False,None)
                    variable_set.append(v)

                eq = set(variable_set) 

                clue_counter += 1
                add_key = Key(location,clue_counter,clue)
                KB[add_key] = eq


    return KB


def advanced_solver(KB,minMap,d,n):
    identified_mines = []
    tripped_mines = []
    visited = set()
    inferenced_cells = set()
    i = 0
    clue_counter = 0
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
        
        
        if revealed:
            print("---REBUILDING KNOWLEDGE BASE---")
            KB = rebuild_KB(KB,minMap,inferenced_cells)
            clue_counter = len(KB)
            for k in KB:
                print((k,KB[k]))
        
        if not revealed:
            (KB,minMap,flagged_mines,anything_assigned) = subset_solver(KB,minMap,clue_counter,inferenced_cells)
            identified_mines.extend(flagged_mines)
            if anything_assigned:
                revealed = True
            i += len(flagged_mines)
        
        if i>=n:
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
        #input("---------------------------------------->")
        printTimeSteps(minMap,d)

    return (identified_mines,tripped_mines)
def advanced_solver_play_by_play(KB,minMap,d,n):
    identified_mines = []
    tripped_mines = []
    visited = set()
    inferenced_cells = set()
    i = 0
    clue_counter = 0
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
        
        
        if revealed:
            print("---REBUILDING KNOWLEDGE BASE---")
            KB = rebuild_KB(KB,minMap,inferenced_cells)
            clue_counter = len(KB)
            for k in KB:
                print((k,KB[k]))
        
        if not revealed:
            (KB,minMap,flagged_mines,anything_assigned) = subset_solver(KB,minMap,clue_counter,inferenced_cells)
            identified_mines.extend(flagged_mines)
            if anything_assigned:
                revealed = True
            i += len(flagged_mines)
        
        if i>=n:
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
        input("---------------------------------------->")
        printTimeSteps(minMap,d)

    return (identified_mines,tripped_mines)

def heuristic_assignments(KB,board,eq,clue):
    #Checks if there is any possible assignment for variables based on length. To understand: Use A  + B = Clue val and A - B = Clue val for length = 2 and generate all possible combinations for 0 and 1
    assignment_set = []
    #--Based on length of eq, return possible assignments for variables if any
    #print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    if len(eq) == 1: 
        variable = None
        for e in eq:
            variable = e
            break
        if clue == 1:
            variable.assignment = 1
        else:
            variable.assignment = 0

        assignment_set.append(variable)

    elif len(eq) == 2:
        negative_counter = 0
        for e in eq:
            negative_counter += 1 if e.isNegative == True else 0

        if clue == 0:
            if negative_counter == 0 or negative_counter == 2:
                for e in eq:
                    e.assignment = 0
                    assignment_set.append(e)
            if negative_counter == 1:
                for e in eq:
                    e.assignment = 1
                    assignment_set.append(e)
    
        if clue == 1:
            if negative_counter == 1:
                for e in eq:
                    if e.isNegative:
                        e.assignment = 0
                    else:
                        e.assignment = 1
                    
                    assignment_set.append(e)
        
        if clue == 2:
            for e in eq:
                e.assignment = 1
                assignment_set.append(e)

    elif len(eq) > 2:
        if clue == 0:
            for e in eq:
                assignment_set.append(e)
            return assignment_set
        negative_counter = 0
        for e in eq:
            if e.isNegative == True:
                negative_counter  += 1 

        if negative_counter == len(eq):
            for e in eq:
                e.assignment = 0
                assignment_set.append(e)



    return assignment_set

def updateKB(KB,board,location,safe,identified_mines,mines_found): 
    var = None
    found = False
    #Finds Variable associated with location
    to_remove = []
    for key in KB: 
       
        eq = KB[key]
        for e in eq:
            if e.location == location:
                if safe:
                    eq.remove(e)
                    break
                else:
                    eq.remove(e)
                    key.clue-=1
                    break
        if len(eq) == 0:
            to_remove.append(key)
       
    for r in to_remove:
        KB.pop(r)

    return (KB,identified_mines,mines_found)
                
 
def create_cells_set(d):
    cells_set = set()
    for i in range(d):
        for j in range(d):
            cells_set.add((i,j))

    return cells_set

def make_basic_inferences(KB,board,eq,key, identified_mines,inferenced_cells):
    
    key_location = key.location
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j].location == key_location:
                cell = board[i][j]
    assignment_set = []
    
    #MAKE BASIC INFERENCES USING INFERENCE IF STATEMENTS
    if cell.visited == 1 and not cell.location in inferenced_cells:
        
        cell.clue = getClue(board,cell)
        cell.revealedMines =  revealedMines(board, cell)
        cell.numHiddenSquares =  hiddenCells(board, cell)
        neighbors = getNeighbors(board,cell)
        cell.numSafeNeighbors = revealedSafeNeighbors(board, cell)
        
        if (cell.clue - cell.revealedMines == cell.numHiddenSquares):
           
            neighbors = getNeighbors(board,cell)
            
            for c in neighbors:
                print("all mines")
                if c.visited == 0:
                    c.visited = 2
                    if not c.location  in identified_mines:
                        identified_mines.append(c.location)
                    
                    assignment_set.append(Variable(c.location,None,1))
            inferenced_cells.append(cell.location)
            revealed = True

            #added = True
           # print("random i val check: ", end = ' ')
           # print(i)

        elif ((len(neighbors)- cell.clue) - cell.numSafeNeighbors == cell.numHiddenSquares):
            print("all safe")
            for c in neighbors:
               
                if c.visited == 0 :
                    c.visited = 1
                   
                    assignment_set.append(Variable(c.location,None,0))
            inferenced_cells.append(cell.location)

    return (assignment_set,identified_mines,inferenced_cells)

#ADVANCED INFERENCES USING GAUSSIAN ELIMINATION
def make_advanced_inferences(KB,board,matrix):
    n = np.array(matrix)
    M = Matrix(n) 
 
    #Returns rref matrix and pivot columns as tuple
    temp_tuple = M.rref()

    #extracts matrix from tuple
    reduced_matrix = np.array(temp_tuple[0])
    print("regular matrix: ")
    print(np.array(M))
    print("reduced matrix")
    print(reduced_matrix)
    #ADD LOCATIONS OF ANY ASSIGNMENTS IN LOCATION LIST
    locations_list = []
    for i in range(len(reduced_matrix)):
        
        temp_list = []
        for j in range(len(reduced_matrix)):
            if reduced_matrix[i][j] == 1:
                temp_list.append(((i,j),reduced_matrix[i][ len(reduced_matrix)-1]))
        
        if len(temp_list) == 1:
            locations_list.extend(temp_list)
    
    #ADD LOCATIONS LIST TO VARIABLES LIST
    var_list = []
    for l in locations_list:
        location = l[0]
        assignment = l[1]
        var = Variable(location,None,assignment)
        var_list.append(var)

    return var_list


#ADVANCED AGENT 
def matrix_advanced_agent(KB,board,d,n):
    cells_set = create_cells_set(d)
    identified_mines = []
    tripped_mines = []
    mines_found = 0
    clue_counter = 0
    while (mines_found < n):
        revealed = False
        assignment_set = []
        matrix = []

        #INFERENCE STEP
        inferenced_cells = []
        for key in KB:
            inference_type = -1
            eq = KB[key]
            beginning_len = len(assignment_set)
            (basic_assignments,t_i_mines,i_cells) = (make_basic_inferences(KB,board,eq,key,identified_mines,inferenced_cells))
            inferenced_cells.extend(i_cells)
            assignment_set.extend(basic_assignments)
            identified_mines.extend(t_i_mines)

            if len(assignment_set) > beginning_len:
                print("---MADE BASIC INFERENCES---\n")
                inference_type = 0
                #ADD TO INFERENCED CELLS SET TO REMOVE LATER FROM KB 
                inferenced_cells.append(key.location)
                continue 
            else:
                #print("--MAKING ADVANCED INFERENCES--")
                row = []
                location_set = []
                for e in eq:
                    location_set.append(e.location)
                for c in cells_set:
                    row.append(0 if not c in location_set else 1)
                row.append(key.clue)

                matrix.append(row)
        
        advanced_inferences = make_advanced_inferences(KB,board,matrix)
        assignment_set.extend(advanced_inferences)
        if len(assignment_set) > 0:
            if inference_type == -1:
                inference_type = 1
                print("--MADE ADVANCED INFERENCES--\n")

            print("--FOUND ASSIGNMENTS FOR VARIABLES--")
            revealed = True

        for k in KB:
            print((k,KB[k]))
        #TO DELETE LIST
        to_delete = []
        for k in KB:
            if k.location in inferenced_cells:
                to_delete.append(k)

        for t in to_delete:
            KB.pop(t)
                
           
        #ASSIGNMENT STEP / REDUCTION STEP
        to_remove = []
        for assignment in assignment_set: 
            to_remove  = []
            for keyC in KB:
                eq = KB.get(keyC)
               
                if assignment in eq:
                    if assignment.assignment == 1:
                        keyC.clue -= 1
                        identified_mines.append(assignment.location)
                        x = assignment.location[0]
                        y = assignment.location[1]
                        board[x][y].visited = 2
                        mines_found  += 1

                    eq.remove(assignment) #position of this statement and the above subject to change
                   
                    if len(eq) == 0:
                        to_remove.append(keyC)
                       

            for r in to_remove:
                KB.pop(r)

        #REVEAL SAFE NEIGHBORS AND ADD TO KB
        for assignment in assignment_set:
            if assignment.assignment == 0:
                location = assignment.location 
                print("out of range??"  + str((x,y)))
                rowX = location[0]
                colX = location[1]
                board[rowX][colX].visited = 1
                
                clue_temp = getClueV2(board,location)
                clue = clue_temp - revealedMinesV2(board,location)
                board[x][y].clue = clue
                hiddenNeighbors = getHiddenNeighbors(board,location)
                
                
                #This will be objects. Could take up multiple lines of code to make them into objects though.
                #Will be hashed based on location
                #Create new Variable objects for each of the hidden neighbors based on location
                variable_set = []
                for neighbor in hiddenNeighbors:
                    v = Variable(neighbor,False,None)
                    variable_set.append(v)

                eq = set(variable_set) 

                clue_counter += 1
                add_key = Key(location,clue_counter,clue)
                KB[add_key] = eq
        
        #CHECK MINES
        if mines_found >= n:
            break

        #RANDOM ASSIGHNEMENT
        if not revealed:
            remainingCells = set()
            for r in range(len(board)):
                for c in range(len(board)):
                    if  board[r][c].visited == 0:
                        remainingCells.add(board[r][c].location)

            if len(remainingCells) > 0:
                random_location  = random.choice(tuple(remainingCells))
                xRand = random_location[0]
                yRand = random_location[1]
                random_cell = board[xRand][yRand]
                location = board[xRand][yRand].location 

                x = location[0]
                y = location[1]
                if random_cell.safe:
                    
                    board[x][y].visited = 1
                   

                    clue_temp = getClueV2(board,location) 
                   
                    clue = clue_temp - revealedMinesV2(board,location) 
                    board[x][y].clue = clue
                    hiddenNeighbors = getHiddenNeighbors(board,location)
                
                    (KB,identified_mines,mines_found) = updateKB(KB,board,location,False,identified_mines,mines_found)
                    #This will be objects. Could take up multiple lines of code to make them into objects though.
                    #Will be hashed based on location
                    #Create new Variable objects for each of the hidden neighbors based on location
                    variable_set = []
                    for neighbor in hiddenNeighbors:
                        v = Variable(neighbor,False,None)
                        variable_set.append(v)

                    eq = set(variable_set) 
                    
                    clue_counter += 1
                    key = Key(location,clue_counter,clue)
                    KB[key] = eq
                        #---#Create equation for the Cell---
                            #Includes creating new instance of Variable object (see line 443 for example)
                            #and adding it to the KB by incrementing the clue counter
                else:
                    board[xRand][yRand].visited = -1
                    tripped_mines.append(random_cell.location)
                    (KB,identified_mines,mines_found) = updateKB(KB,board,location,False,identified_mines,mines_found)
                    mines_found += 1  
        
            else:
                break
        input("------------------------------------------------------------------------------------------>")
      
        printTimeSteps(board,d)  
        print("Identified Mines: ", end = ' ')
        print(identified_mines)
        print("Tripped Mines: ", end = ' ')
        print(tripped_mines)
        print(str(mines_found) + " / " + str(n) + " mines found")
        


    return (identified_mines,tripped_mines)



def play_by_play(d,n):
    board = createBoard(n,d)
    KB = {}
    (identified,tripped) = advanced_solver_play_by_play(KB,board,d,n)

    print("Identified mines : ", end = '\t')
    print(identified)
    print("Tripped mines : ", end = '\t')
    print(tripped)
    print("Success Rate: ")
    print(float(len(identified)/float(n)))


#board = createBoard(n,d)

print("Select an option: ")
print("1: Comparison of success rates between Basic and Advanced Agents (dim = user defined) and (number of mines = user defined) ")
print("2: Play by Play of Basic or Advanced Agents")
option = int(input("--------------------------------------------------------------------------------------------------------------\n"))
if option == 2:
    d = int(input("Enter dimension size: \n"))
    n = int(input("Enter number of mines: \n"))
    play_by_play(d,n)
else:
    solver_option = int(input("Which Success rate do you want to see?: \n(1) Basic Agent \n(2) Advanced Agent\n"))
    d = int(input("select dimension size: \n"))
    n = int((input("select number of mines: \n")))

    if solver_option == 2:
        success_rate = []
        total_rate = []
        scores = []
        counter = 0
        for i in range(10):
            minMap = createBoard(n, d)
            KB = {}
            (identified, tripped) = advanced_solver(KB,minMap,d,n)
        
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
        '''
        for i in range(len(minMap)):
            for j in range(len(minMap)):
                print(minMap[i][j].visited, end = '\t')

            print('\n')
        '''
        success = ((sum(success_rate)))
        total =  (sum(total_rate))
        print(counter)
        rate = float(float(success)/ float(total))
        print("success rate: ", end = '\t')
        print(rate)

    elif solver_option == 1:
        success_rate = []
        total_rate = []
        scores = []
        counter = 0
        for i in range(10):
            minMap = createBoard(n, d)
            KB = {}
            (identified, tripped) = solver(minMap,d,n)
        
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
        '''
        for i in range(len(minMap)):
            for j in range(len(minMap)):
                print(minMap[i][j].visited, end = '\t')

            print('\n')
        '''
        success = ((sum(success_rate)))
        total =  (sum(total_rate))
        print(counter)
        rate = float(float(success)/ float(total))
        print("success rate: ", end = '\t')
        print(rate)

    else:
        print("Invalid option(s) selection")






