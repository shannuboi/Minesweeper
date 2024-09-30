import pygame
import random
pygame.init()

# Game settings
Game_Width = 10
Game_Height = 10
totMines = 9

Dimension = 32  # Also The size of the sprites
LRBorder = 10   # Left Right Border
TDBorder = 75   # Top Down Border (extra space for game text)

# Setting the display
Display_Width = Dimension * Game_Width + LRBorder * 2
Display_Height = Dimension * Game_Height + TDBorder * 2
mainDisplay = pygame.display.set_mode((Display_Width, Display_Height))
BackgroundColor = (1, 1, 13)

pygame.display.set_caption("Minesweeper")
iconImg = pygame.image.load("Sprites/icon.png")
pygame.display.set_icon(iconImg)

minePos = []
# [(x, y), (x, y), ...]

grid = []
# [[[val, clicked, flagged, rect, (x, y)], [...], ...],
# [[...], [...], ...],
# .     .
# .        .
# .           .
# [[...], [...], ...]]


# Draw game sprites from Sprites folder
def draw_gridbox(gridbox):  # The function takes in a gridbox (which is a list) as an argument
    if gridbox[1]:
    # if clicked
        if gridbox[0] == -1:    # <-- This statement checks what type of gridbox it is.
                                # Values from 0-8 represent the numbers 0 to 8 and -1 represents a mine
            # display.blit puts the image on to a specified position
            mainDisplay.blit(pygame.image.load("Sprites/mine.png"), gridbox[3])
        if gridbox[0] == 0:
            mainDisplay.blit(pygame.image.load("Sprites/empty.png"), gridbox[3])
        if gridbox[0] == 1:
            mainDisplay.blit(pygame.image.load("Sprites/grid1.png"), gridbox[3])
        if gridbox[0] == 2:
            mainDisplay.blit(pygame.image.load("Sprites/grid2.png"), gridbox[3])
        if gridbox[0] == 3:
            mainDisplay.blit(pygame.image.load("Sprites/grid3.png"), gridbox[3])
        if gridbox[0] == 4:
            mainDisplay.blit(pygame.image.load("Sprites/grid4.png"), gridbox[3])
        if gridbox[0] == 5:
            mainDisplay.blit(pygame.image.load("Sprites/grid5.png"), gridbox[3])
        if gridbox[0] == 6:
            mainDisplay.blit(pygame.image.load("Sprites/grid6.png"), gridbox[3])
        if gridbox[0] == 7:
            mainDisplay.blit(pygame.image.load("Sprites/grid7.png"), gridbox[3])
        if gridbox[0] == 8:
            mainDisplay.blit(pygame.image.load("Sprites/grid8.png"), gridbox[3])
    else:
        if gridbox[2]:
        # if flagged
            mainDisplay.blit(pygame.image.load("Sprites/flag.png"), gridbox[3])
        else:
            mainDisplay.blit(pygame.image.load("Sprites/Grid.png"), gridbox[3])


# For all non-mines, this function gives the value (i.e. the number of mines around that gridbox) 
def give_val_to_gridbox(gridbox):   # The function takes in a gridbox (which is a list) as an argument
    if gridbox[0] != -1:    # If not a mine
        # Loop through all 8 gridboxes around the current gridbox
        for i in range(-1, 2):
            for j in range(-1, 2):
                xpos = gridbox[4][0] + i
                ypos = gridbox[4][1] + j
                in_grid = 0 <= xpos < Game_Width and 0 <= ypos < Game_Height
                if in_grid and grid[xpos][ypos][0] == -1:
                    gridbox[0] += 1


# When a gridbox is clicked it needs to be revealed. If the gridbox revealed has a value of 0 then
# (like in the original windows minesweeper) we need to reveal all non mines around it. To do this
# the function will call itself on the new gridbox.
def show_gridbox(gridbox):   # The function takes in a gridbox (which is a list) as an argument
    gridbox[1] = True

    if gridbox[0] == 0:
        for i in range(-1, 2):
            for j in range(-1, 2):
                xpos = gridbox[4][0] + i
                ypos = gridbox[4][1] + j
                in_grid = 0 <= xpos < Game_Width and 0 <= ypos < Game_Height
                if in_grid and not grid[xpos][ypos][1]: # in grid and not a mine
                    show_gridbox(grid[xpos][ypos])  # Function recalling itself

# If one mine is revealed then all other mines need to be revealed as well.
    elif gridbox[0] == -1:
        for m in minePos:
            if not grid[m[0]][m[1]][1]:   # If not already shown
                show_gridbox(grid[m[0]][m[1]])  # Then show it


def main():
    running = True
    gameOver = False
    gameWon = False

    global grid
    grid = []
    global minePos
    minesLeft = totMines

# Genaratign mines:
    # First mine is genarated here
    minePos = [(random.randrange(0, Game_Width), random.randrange(0, Game_Height))]

    # Looping to generate the rest of the mines
    for i in range(totMines - 1):
        temp_pos = (random.randrange(0, Game_Width), random.randrange(0, Game_Height))  # give temp pos
        present = True
        # Compare with previos mines to check if genarated temp pos is already in the list
        while present:
            for j in range(len(minePos)):
                if temp_pos == minePos[j]:
                    temp_pos = (random.randrange(0, Game_Width), random.randrange(0, Game_Height))
                    break
                if j == len(minePos) - 1:
                    present = False
        minePos.append(temp_pos)

# Creating the grid:
    for i in range(Game_Height):
        line = []
        for j in range(Game_Width):
            rect = pygame.Rect(LRBorder + i * Dimension, TDBorder + j * Dimension, Dimension, Dimension)
            if (i, j) in minePos:
                line.append([-1, False, False, rect, (i, j)])
            else:
                line.append([0, False, False, rect, (i, j)])
        grid.append(line)

    for i in grid:
        for j in i:
            give_val_to_gridbox(j)

# Game loop:
    while running:
        mainDisplay.fill(BackgroundColor)   # clear the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:   # Code to exit the game
                running = False
            if gameOver or gameWon:     # Code to reset the game 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        running = False
                        main()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in grid:
                        for j in i:
                            if j[3].collidepoint(event.pos):
                                if event.button == 1:   # code to click a box
                                    if not j[2]:
                                        show_gridbox(j)
                                        if j[0] == -1:
                                            gameOver = True
                                if event.button == 3:   # code to flag a box
                                    if not j[1]:
                                        if j[2]:
                                            j[2] = False
                                            minesLeft += 1
                                        else:
                                            j[2] = True
                                            minesLeft -= 1

        # Checking if game is won
        gameWon = True
        for i in grid:
            for j in i:
                draw_gridbox(j)
                if j[0] != -1 and not j[1]:    # if every non-mine is clicked
                    gameWon = False

        # Game text
        FONT = pygame.font.SysFont("Calibri", 25, bold = True)

        if gameOver:
            # Game over text
            text = FONT.render("You Lost", False, (255, 255, 255))
            mainDisplay.blit(text, (LRBorder, TDBorder + Dimension * Game_Height + 10))
            text = FONT.render("Press R to restart", False, (255, 255, 255))
            mainDisplay.blit(text, (LRBorder, Display_Height - 25))
        elif gameWon:
            # Game won text
            text = FONT.render("You Won", False, (255, 255, 255))
            mainDisplay.blit(text, (LRBorder, TDBorder + Dimension * Game_Height + 10))
            text = FONT.render("Press R to restart", False, (255, 255, 255))
            mainDisplay.blit(text, (LRBorder, Display_Height - 25))

        # Game state text
        text = FONT.render("Mines left: " + str(minesLeft), False, (255, 255, 255))
        mainDisplay.blit(text, (LRBorder, LRBorder))

        pygame.display.update()


main()
pygame.quit()
