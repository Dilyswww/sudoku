import pygame
import time
pygame.font.init()

class Grid:
    """
    Represents the Sudoku board and game logic
    """
    # A standard board with initial given values
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]
    
    def __init__(self, rows, cols, width, height, win):
        """
        Initializes the Sodoku grid
        """
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win
 
    def update_model(self):
        """
        Updates the internal model with cube values.
        """
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]
        
    def place(self, val):
        """
        Places a value in the selected cube and validates the move.

        Args:
            val (int): The value to be placed.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()
            
            if valid(self.model, val, (row, col)) and self.solve():
                return True
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False
            
    def sketch(self, val):
        """
        Sets a temporary value in the selected cube.

        Args:
            val (int): The temporary value to be set.
        """
        row, col = self.selected
        self.cubes[row][col].set_temp(val)
        
    def draw(self):
        """
        Draws the Sudoku grid, including grid lines and cube values.
        """
        # Draw grid lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            
        # Draw cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)
                
    def select(self, row, col):
        """
        Selects a cube at the specified row and column.

        Args:
            row (int): Row index of the cube.
            col (int): Column index of the cube.
        """
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
                
        self.cubes[row][col].selected = True
        self.selected = (row, col)
        
    def clear(self):
        """
        Clears the temporary value of the selected cube.
        """
        row, col = self.selected
        if self.cubes[row][col].value!= 0:
            self.cubes[row][col].set_temp(0)
            
    def click(self, pos):
        """
        Converts mouse position to row and column indices.

        Args:
            pos (tuple): The mouse position (x, y) in pixels.

        Returns:
            tuple: Row and column indices corresponding to the position, or None if outside the grid.
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None
        
    def is_finished(self):
        """
        Checks if the Sudoku grid is fully filled.

        Returns:
            bool: True if the grid is fully filled, False otherwise.
        """
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True
        
    def solve(self):
        """
        Solves the Sudoku grid using a backtracking algorithm.

        Returns:
            bool: True if a solution is found, False otherwise.
        """
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find
            
        for val in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                
                if self.solve():
                    return True
                
                self.model[row][col] = 0
                
        return False
    
    def solve_game(self):
        """
        Solves the Sudoku game by updating the display step by step.

        Returns:
            bool: True if the game is solved, False otherwise.
        """
        self.update_model()
        find = find_empty(self.model)
        if not find:
            return True
        else:
            row, col = find
            
        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)
                
                if self.solve_game():
                    return True
                
                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)
                
        return False
            
class Cube:
    
    """
    A single cube in a Sudoku puzzle.
    """
    
    rows = 9
    cols = 9
    
    def __init__(self, value, row, col, width, height):
        """
        Initializes a Cube instance.

        :param value: The value of the cube (0 for empty).
        :param row: The row index of the cube in the puzzle grid.
        :param col: The column index of the cube in the puzzle grid.
        :param width: The width of the cube.
        :param height: The height of the cube.
        """
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False
        
    def draw(self, win):
        """
        Draws the cube on the given window.

        :param win: The Pygame window on which to draw the cube.
        """
        fnt = pygame.font.SysFont("comicsans", 40)
        
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2). y +(gap / 2 - text.get_height() / 2)))
            
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)
            
    def draw_change(self, win, g = True):
        """
        Draws a changed cube state on the given window.

        :param win: The Pygame window on which to draw the cube.
        :param g: If True, the cube is drawn with a green border; otherwise, with a red border.
        """
        fnt = pygame.fon.SysFont("comicsans", 40)
        
        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap
        
        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)
        
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2). y +(gap / 2 - text.get_height() / 2)))
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)
        
    def set(self, val):
        self.value = val
        
    def set_temp(self, val):
        self.temp = val
        
    def find_empty(bo):
        """
        Finds the coordinates of the first empty cube in the puzzle.

        :param bo: The Sudoku puzzle grid.
        :return: The row and column indices of the empty cube, or None if no empty cube is found.
        """
        for i in range(len(bo)):
            for j in range(len(bo[0])):
                if bo[i][j] == 0:
                    return (i, j) # row, col
                
        return None
        
    def valid(bo, num, pos):
        """
        Checks if placing a number in a given position is valid.

        :param bo: The Sudoku puzzle grid.
        :param num: The number to be checked for validity.
        :param pos: The position (row, column) to be checked.
        :return: True if the number can be placed in the given position, False otherwise.
        """
        # Check row
        for i in range(len(bo[0])):
            if bo[pos[0]][i] == num and pos[1] != i:
                return False
            
            
        # Check column
        for i in range(len(bo)):
            if bo[i][pos[1]] == num and pos[0]!= i:
                return False
            
        # Check 3x3 box
        box_x = pos[1] // 3
        box_y = pos[0] // 3
        
        for i in range(box_y * 3, box_y * 3 + 3):
            for j in range(box_x * 3, box_x * 3 + 3):
                if bo[i][j] == num and (i, j) != pos:
                    return False
            
        return True
    
    def redraw_window(win, board, time, strikes):
        """
        Redraws the entire game window.

        :param win: The Pygame window.
        :param board: The Sudoku board instance.
        :param time: The elapsed time.
        :param strikes: The number of strikes.
        """
        win.fill((255, 255,255))
        
        # Draw time
        fnt = pygame.font.SysFont("comicsans", 20)
        text = fnt.render("Time: " + format_time(time), 1, (0, 0, 0))
        win.blit(text, (400, 560))
        
        # Draw strikes
        text = fnt.render("X " * strikes, 1, (255, 0, 0))
        win.blit(text, (20, 560))
        
        # Draw grid and board
        board.draw()
        
    def format_time(secs):
        """
        Formats the elapsed time into a human-readable string.

        :param secs: The elapsed time in seconds.
        :return: The formatted time string.
        """
        sec = sec % 60
        min = secs // 60
        hour = min // 60
        
        mat = " " + str(min) + ":" + str(sec)
        return mat
    
def main():
    """
    Solves the sudoku problem.
    """
    win = pygame.display.set_model((540, 600))
    pygame.display.set_caption("Sudoku")
    board = Grid(9, 9, 540, 540, win)
    key = None
    run = True
    start = time.time()
    strikes = 0
    
    while run:
        play_time = round(time.time() - start)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            # Handle key presses
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                    
                
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                    
                    
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                    
                if event.key == pygame.K_SPACE:
                    board.solve_game()
                
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None
                        
                        if board.is_finished():
                            print("Game over")
    
                # Handle mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    clicked = board.click(pos)
                    if clicked:
                        board.select(clicked[0], clicked[1])
                        key = None
                
            # If a cube is selected and a key is pressed, sketch the value
            if board.selected and key != None:
                board.sketch(key)
                
            # Redraw the window and update the display
            redraw_window(win, board, play_time, strikes)
            pygame.display.update()        
            
            
main()
pygame.quit()