import pygame
from Minesweeper_utilities import *
from tkinter import *
from tkinter import messagebox

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

dim = int(input("Dimension Size: "))
n = int(input("Enter number of mines: " ))
# This sets the WIDTH and HEIGHT of each grid location
WIDTH = int((500 / dim)) - 5
HEIGHT = int((500 / dim )) - 5
 
# This sets the margin between each cell
MARGIN = 5

# Create a 2 dimensional array. A two dimensional
# array is simply a list of lists.
grid = []
for row in range(dim):
    # Add an empty array that will hold each cell
    # in this row
    grid.append([])
    for column in range(dim):
        grid[row].append(0)  # Append a cell
 
# Set row 1, cell 5 to one. (Remember rows and
# column numbers start at zero.)

 
# Initialize pygame
pygame.init()


myfont = pygame.font.SysFont('Comic Sans MS', int(WIDTH / 5))
# Set the HEIGHT and WIDTH of the screen
WINDOW_SIZE = [500, 500]
screen = pygame.display.set_mode(WINDOW_SIZE)
 
# Set title of screen
pygame.display.set_caption("Minesweeper")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()


KB = {}
minMap = createBoard(n,dim)

visited = set()
inferenced_cells = set()
clue_counter = 0
identified_mines = []
tripped_mines = []
i = 0


sysfont = pygame.font.get_default_font()

font = pygame.font.SysFont(None, int(WIDTH))


 
# -------- Main Program Loop -----------

game_over = False
while not done:
    if game_over:
        Tk().wm_withdraw() #to hide the main window
        messagebox.showinfo('GAME OVER','OK')
        done = True
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            done = True  # Flag that we are done so we exit this loop
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            
            
            (minMap,KB,identified,tripped,i,visited,inferenced_cells,clue_counter) = advanced_solver(KB,minMap,dim,n,visited,inferenced_cells,clue_counter,i)

            identified_mines.extend(identified)
            tripped_mines.extend(tripped)
            if i >= n:
               game_over = True
            
            for x in range(dim):
                for y in range(dim):
                    grid[x][y] = int(minMap[x][y].visited)
            
 
    # Set the screen background
    #screen.fill(BLACK)
    
    # Draw the grid
    
    for row in range(dim):
        for column in range(dim):
            if grid[row][column] ==0:
                color = WHITE
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])          
                                
            elif grid[row][column] == 2:
                color = RED
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
            elif grid[row][column] == -1:
                color = BLACK
                pygame.draw.rect(screen,
                                color,
                                [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
            
            elif grid[row][column] == 1:
                 #print(minMap[row][column].clue)
                 color = GREEN
                 clue = int(minMap[row][column].clue)
                 img = font.render(str(clue), True, BLACK)
                 
                 screen.blit(img, [(MARGIN + WIDTH) * column + MARGIN,
                                (MARGIN + HEIGHT) * row + MARGIN,
                                WIDTH,
                                HEIGHT])
                
                 #pygame.display.update()
            
  
            
 
    # Limit to 60 frames per second
    clock.tick(60)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
# Be IDLE friendly. If you forget this line, the program will 'hang'
# on exit.

#pygame.quit()
print("Total Score: " + str(len(identified_mines))+ " / " + str(n) + " mines flagged")
print("Identified Mines: ", end = ' ')
print((identified_mines))
print("Tripped Mines: ", end =  ' ')
print(tripped_mines)
