import pygame
import sys
import time
from solver import Cell, Sudoku
from level import Level
from button_sprite import ButtonSprite


pygame.init()

# Set size of game and other constants
cell_size = 50
minor_grid_size = 1
major_grid_size = 3
buffer = 5
button_height = 50
button_width = 125
button_border = 2
width = cell_size*9 + minor_grid_size*6 + major_grid_size*4 + buffer*2
height = cell_size*9 + minor_grid_size*6 + \
    major_grid_size*4 + button_height + buffer*3 + button_border*2
size = width, height
white = 255, 255, 255
black = 0, 0, 0
gray = 200, 200, 200
green = 0, 175, 0
red = 200, 0, 0
inactive_btn = 51, 255, 255
active_btn = 51, 153, 255

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Sudoku')


class RectCell(pygame.Rect):
    '''
    A class built upon the pygame Rect class used to represent individual cells in the game.
    This class has a few extra attributes not contained within the base Rect class.
    '''

    def __init__(self, left, top, row, col):
        super().__init__(left, top, cell_size, cell_size)
        self.row = row
        self.col = col


def create_cells():
    '''Creates all 81 cells with RectCell class.'''
    cells = [[] for _ in range(9)]

    # Set attributes for for first RectCell
    row = 0
    col = 0
    left = buffer + major_grid_size
    top = buffer + major_grid_size

    while row < 9:
        while col < 9:
            cells[row].append(RectCell(left, top, row, col))

            # Update attributes for next RectCell
            left += cell_size + minor_grid_size
            if col != 0 and (col + 1) % 3 == 0:
                left = left + major_grid_size - minor_grid_size
            col += 1

        # Update attributes for next RectCell
        top += cell_size + minor_grid_size
        if row != 0 and (row + 1) % 3 == 0:
            top = top + major_grid_size - minor_grid_size
        left = buffer + major_grid_size
        col = 0
        row += 1

    return cells


def draw_grid():
    '''Draws the major and minor grid lines for Sudoku.'''
    # Draw minor grid lines
    lines_drawn = 0
    pos = buffer + major_grid_size + cell_size
    while lines_drawn < 6:
        pygame.draw.line(screen, black, (pos, buffer),
                         (pos, width-buffer-1), minor_grid_size)
        pygame.draw.line(screen, black, (buffer, pos),
                         (width-buffer-1, pos), minor_grid_size)

        # Update number of lines drawn
        lines_drawn += 1

        # Update pos for next lines
        pos += cell_size + minor_grid_size
        if lines_drawn % 2 == 0:
            pos += cell_size + major_grid_size

    # Draw major grid lines
    for pos in range(buffer+major_grid_size//2, width, cell_size*3 + minor_grid_size*2 + major_grid_size):
        pygame.draw.line(screen, black, (pos, buffer),
                         (pos, width-buffer-1), major_grid_size)
        pygame.draw.line(screen, black, (buffer, pos),
                         (width-buffer-1, pos), major_grid_size)


def fill_cells(cells, board):
    '''Fills in all the numbers for the game.'''
    font = pygame.font.Font(None, 36)

    # Fill in all cells with correct value
    for row in range(9):
        for col in range(9):
            if board.board[row][col].value is None:
                continue

            # Fill in given values
            if not board.board[row][col].editable:
                font.bold = True
                text = font.render(f'{board.board[row][col].value}', 1, black)

            # Fill in values entered by user
            else:
                font.bold = False
                if board.check_move(board.board[row][col], board.board[row][col].value):
                    text = font.render(
                        f'{board.board[row][col].value}', 1, green)
                else:
                    text = font.render(
                        f'{board.board[row][col].value}', 1, red)

            # Center text in cell
            xpos, ypos = cells[row][col].center
            textbox = text.get_rect(center=(xpos, ypos))
            screen.blit(text, textbox)


def draw_board(active_cell, cells, game):
    '''Draws all elements making up the board.'''
    # Draw grid and cells
    draw_grid()
    if active_cell is not None:
        pygame.draw.rect(screen, gray, active_cell)

    # Fill in cell values
    fill_cells(cells, game)


def visual_solve(game, cells):
    '''Solves the game while giving a visual representation of what is being done.'''
    # Get first empty cell
    cell = game.get_empty_cell()

    # Solve is complete if cell is False
    if not cell:
        return True

    # Check each possible move
    for val in range(1, 10):
        # Allow game to quit when being solved
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        # Place value in board
        cell.value = val

        # Outline cell being changed in red
        screen.fill(white)
        draw_board(None, cells, game)
        cell_rect = cells[cell.row][cell.col]
        pygame.draw.rect(screen, red, cell_rect, 5)
        pygame.display.update([cell_rect])
        time.sleep(0.05)

        # Check if the value is a valid move
        if not game.check_move(cell, val):
            cell.value = None
            continue

        # If all recursive calls return True then board is solved
        screen.fill(white)
        pygame.draw.rect(screen, green, cell_rect, 5)
        draw_board(None, cells, game)
        pygame.display.update([cell_rect])
        if visual_solve(game, cells):
            return True

        # Undo move is solve was unsuccessful
        cell.value = None

    # No moves were successful
    screen.fill(white)
    pygame.draw.rect(screen, white, cell_rect, 5)
    draw_board(None, cells, game)
    pygame.display.update([cell_rect])
    return False


def check_sudoku(sudoku):
    '''
    Takes a complete instance of Soduku and 
    returns whether or not the solution is valid.
    '''
    # Ensure all cells are filled
    if sudoku.get_empty_cell():
        raise ValueError('Game is not complete')

    # Will hold values for each row, column, and box
    row_sets = [set() for _ in range(9)]
    col_sets = [set() for _ in range(9)]
    box_sets = [set() for _ in range(9)]

    # Check all rows, columns, and boxes contain no duplicates
    for row in range(9):
        for col in range(9):
            box = (row // 3) * 3 + col // 3
            value = sudoku.board[row][col].value

            # Check if number already encountered in row, column, or box
            if value in row_sets[row] or value in col_sets[col] or value in box_sets[box]:
                return False

            # Add value to corresponding set
            row_sets[row].add(value)
            col_sets[col].add(value)
            box_sets[box].add(value)

    # All rows, columns, and boxes are valid
    return True


def play(level):
    '''Contains all the functionality for playing a game of Sudoku.'''
    game = Sudoku(level.board)
    cells = create_cells()
    active_cell = None
    solve_rect = pygame.Rect(
        buffer,
        height-button_height - button_border*2 - buffer,
        button_width + button_border*2,
        button_height + button_border*2
    )
    all_sprites = pygame.sprite.Group() 
    solve_btn_sprite = ButtonSprite(all_sprites, 'load.png', 'load_pressed.png',
                              width - buffer*2 - button_border*4 - button_width*2,
                              height - button_height - button_border*2 - buffer,
                              button_width + 5,
                              button_height + 5)
    reset_btn_sprite = ButtonSprite(all_sprites, 'reset.png', 'reset_pressed.png', 
                                    width - buffer - button_border*2 - button_width,
                                    height - button_height - buffer + 3,
                                    button_width + 5,
                                    button_height - 5)
    
    next_level_btn = ButtonSprite(all_sprites, 'next_level.png', 'next_level_pressed.png', 
                                    width - buffer - button_border *2 - button_width * 2.5,
                                    height - button_height - buffer + 3,
                                    button_height - 5,
                                    button_height - 5)
    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 30)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # Handle mouse click
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()

                # Reset button is pressed
                if reset_btn_sprite.rect.collidepoint(mouse_pos):
                    game.reset()

                # Solve button is pressed
                if solve_btn_sprite.rect.collidepoint(mouse_pos):
                    screen.fill(white)
                    active_cell = None
                    draw_board(active_cell, cells, game)
                    all_sprites.draw(screen)
                    all_sprites.update(event)
                    pygame.display.flip()
                    visual_solve(game, cells)

                if next_level_btn.rect.collidepoint(mouse_pos):
                    # TODO сохранить результаты по текущему уровню
                    level.increase()
                    if level.board:
                        game = Sudoku(level.board)
                        cells = create_cells()
                        active_cell = None
                    else:
                        # Конец игры
                        pass

                # Test if point in any cell
                active_cell = None
                for row in cells:
                    for cell in row:
                        if cell.collidepoint(mouse_pos):
                            active_cell = cell

                # Test if active cell is empty
                if active_cell and not game.board[active_cell.row][active_cell.col].editable:
                    active_cell = None

            # Handle key press
            if event.type == pygame.KEYUP:
                if active_cell is not None:

                    # Input number based on key press
                    if event.key == pygame.K_0 or event.key == pygame.K_KP0:
                        game.board[active_cell.row][active_cell.col].value = 0
                    if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        game.board[active_cell.row][active_cell.col].value = 1
                    if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        game.board[active_cell.row][active_cell.col].value = 2
                    if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        game.board[active_cell.row][active_cell.col].value = 3
                    if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        game.board[active_cell.row][active_cell.col].value = 4
                    if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                        game.board[active_cell.row][active_cell.col].value = 5
                    if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                        game.board[active_cell.row][active_cell.col].value = 6
                    if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                        game.board[active_cell.row][active_cell.col].value = 7
                    if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                        game.board[active_cell.row][active_cell.col].value = 8
                    if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                        game.board[active_cell.row][active_cell.col].value = 9
                    if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        game.board[active_cell.row][active_cell.col].value = None

        screen.fill(white)

        # Draw board
        draw_board(active_cell, cells, game)

        # Check if game is complete
        if not game.get_empty_cell():
            if check_sudoku(game):
                # Set the text
                font = pygame.font.Font(None, 36)
                text = font.render('Solved!', 1, green)
                textbox = text.get_rect(center=(solve_rect.center))
                screen.blit(text, textbox)

        # Update screen
        all_sprites.draw(screen)
        all_sprites.update(event)
        text_surface = font.render(f"Уровень {level.level_number}", False, (0, 0, 0))
        screen.blit(text_surface, (20, height - button_height))
        pygame.display.flip()


if __name__ == '__main__':
    level = Level()
    play(level)
