import time
import pygame
import numpy as np


COLOR_BG = (10, 10, 10) # Background color
COLOR_GRID = (40, 40, 40)
COLOR_DIE_NEXT = (170, 170, 170)
COLOR_ALIVE_NEXT = (180, 0 ,141)

# Explanation
# screen: pygame screen
# cells: whole playing field with states for individual cells
# size: size of individual cell
# with_progress = FALSE: when set to false, it will update the screen without setting the next generation of cells
def update(screen, cells, size, with_progress = False):

    # Takes shape of already existing cells and creates an empty array
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    # Allows us to iterate through all individual cells and apply the game rules for Conways game
    for row, col in np.ndindex(cells.shape):

        # Explanation:
        # np.sum(cells[row-1:row+2, col-1:col+2])
            # Counts the total number of alive cells in the area surrounding the current cell (including itself)
            # Notice when you index in Python [1:3] it means 1, 2!
            # Indexing in Python is not inclusive for the upper limit, but is inclusive for the lower limit.
        # cells[row, col]
            # that is a reference to the cell itself, as otherwise, you will include the cell itself in the count
        numNeighborsAlive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]

        # Sets default cell color to the color of the background (COLOR_BG)
        # Sets color to alive if there is an alive cell there
        color = COLOR_BG if cells[row, col] == 0 else COLOR_ALIVE_NEXT

        # Enter condition if there is an alive cell in that position that we are looking at
        if cells[row, col] == 1:
            # Cell is alive but will die next round
            if numNeighborsAlive < 2 or numNeighborsAlive > 3:
                if with_progress:
                    color = COLOR_DIE_NEXT

            # Cell will survive and live onto the next round
            elif 2 <= numNeighborsAlive <= 3:
                # Sets the alive state for the current cell for the next round
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        # Enter condition if there is not an alive cell in the position we are looking at
        else:
            #Enter if the empty cell has 3 alive neighbors and is about to be born
            if numNeighborsAlive == 3:
                # Update the state of the current position to reflect an alive cell in next round
                updated_cells[row, col] = 1
                if with_progress:
                    color = COLOR_ALIVE_NEXT

        # Draw the "rect"angles onto the "screen" with the "color", and draw each rectangle to be the predefined size
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_cells


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))

    # Note how the dimensions are flipped!
    # Define the number of cells
    cells = np.zeros((60, 80))

    # Fills each cell with grid color by default
    screen.fill(COLOR_GRID)

    # The update function will fill the other colors depending on rules we outlined
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False

    #Game Loop that handles key inputs

    # Endless Loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Enter if key is pressed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()

                # If mouse is pressed, we will find out about the position of the
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()
        screen.fill(COLOR_GRID)

        if running:
            cells = update(screen, cells, 10, with_progress = True)
            pygame.display.update()

        time.sleep(0.001)

if __name__ == "__main__":
    main()