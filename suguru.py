import random
import pygame

class Tile:
    def __init__(self, color, number=None, group=None):
        self.number = number
        self.group = group
        self.color = color

    def hasNumber(self):
        return self.number != None

    def inGroup(self):
        return self.group != None


class Suguru:
    def __init__(self, x=3, y=3, block_size=50, background_color=(255, 225, 255)):
        self._x = x
        self._y = y
        self._key = 1

        self._block_size = block_size
        self._width = block_size * x
        self._height = block_size * y
        self._background_color = background_color

        self._color = self._get_random_color()
 
        self._board = [[Tile(self._background_color) for i in range (x)] for j in range (y)]
        self._groups = {}
        
    def Solve(self):
        bo = self._board.copy()
       
        if self._solve(bo, self._groups):
            print("Success")
        else:
            print("Invalid Board")

        self._board = bo

    def Render(self, screen):
        screen.fill(self._background_color)
                
        font = pygame.font.Font('freesansbold.ttf', 32)
        
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                color = self._board[i][j].color
                if self._board[i][j].inGroup():
                    pygame.draw.rect(screen, color, (j * self._block_size, i * self._block_size, self._block_size, self._block_size))
                
                if self._board[i][j].hasNumber():
                    text = font.render(str(self._board[i][j].number), True, (0,0,0), color)
                    textRect = text.get_rect()
                    textRect.center = (self._block_size * j + self._block_size  // 2, self._block_size * i + self._block_size // 2)
                    screen.blit(text, textRect)

        for i in range(self._x):
            pygame.draw.line(screen, (125,125,125), (i * self._block_size, 0), (i * self._block_size, self._height), 2)
        
        for i in range(self._y):
            pygame.draw.line(screen, (125,125,125), (0, i * self._block_size), (self._width, i * self._block_size), 2)
        
        pygame.display.update()

    def GetDimensions(self):
        return (self._width, self._height)

    def InsertNumber(self, num, x, y):
        col = int(x // self._block_size)
        row = int(y // self._block_size)

        self._board[row][col].number = num if num != 0 else None

    def ReadInBoard(self):
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                tile = self._board[i][j]
                if tile.group not in self._groups:
                    self._groups[tile.group] = [[], 1]
                    if tile.hasNumber():
                        self._groups[tile.group][0].append(tile.number)

                elif tile.group in self._groups:
                    self._groups[tile.group][1] += 1
                    if tile.hasNumber():
                        self._groups[tile.group][0].append(tile.number)
    
    def HighlightBoard(self, x, y):
        col = int(x // self._block_size)
        row = int(y // self._block_size)
        
        tile = self._board[row][col]
        tile.group = self._key
        tile.color = self._color 
        
    def IncrementKey(self):
        self._key += 1
        self._color = self._get_random_color()

    def _get_random_color(self):
       random.seed(self._key)
       return tuple([random.randint(0, 255) for _ in range(3)])

    def _solve(self, bo, keys):
        find = self._find_empty(bo)
        if not find:
            return True
        else:
            tag, row, col = find
        for i in range(1, keys[tag][1]+1):
            if self._valid(bo, i, row, col, keys):
                self._board[row][col].number = i

                key_cpy = keys[tag][0].copy()
                keys[tag][0].append(i)

                if self._solve(bo, keys):
                    return True

                bo[row][col].number = None
                keys[tag][0] = key_cpy

        return False

    def _valid(self, bo, num, row, col, keys):
        if num in keys[bo[row][col].group][0]:
            return False

        # If new pos is not in the top or bottom row; check
        if row != 0:
            if bo[row-1][col].number == num:
                return False
            if col != 0:
                if bo[row-1][col-1].number == num:
                    return False
            if col != self._x - 1:
                if bo[row-1][col+1].number == num:
                    return False

        if row != self._y - 1:
            if bo[row+1][col].number == num:
                return False
            if col != 0:
                if bo[row+1][col-1].number == num:
                    return False
            if col != self._x - 1:
                if bo[row+1][col+1].number == num:
                    return False

        if col != 0:
            if bo[row][col-1].number == num:
                return False
        
        if col != self._x - 1:
            if bo[row][col+1].number == num:
                return False

        return True

    def _find_empty(self, bo):
        for i in range(len(bo)):
            for j in range(len(bo[i])):
                if not bo[i][j].hasNumber():
                    return bo[i][j].group, i, j
        return None
