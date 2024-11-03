import pygame
import math
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Path finding algorithm visualized')

RED = (0xff, 0, 0)
GREEN = (0, 0xFF, 0)
BLUE = (0, 0, 0xFF)
YELLOW = (0xFF, 0xFF, 0)
WHITE = (0xFF, 0xFF, 0xFF)
BLACK = (0, 0, 0)
PURPLE = (0x80, 0, 0x80)
ORANGE = (0x80, 0xA5, 0)
GREY = (0X80, 0X80, 0X80)
TURQUOISE = (0x40, 0xE0, 0xD0)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == RED
    
    def is_open(self):
        return self.color == GREEN
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == ORANGE
    
    def is_end(self):
        return self.color == PURPLE
    
    def reset(self):
        self.color == WHITE

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color == BLACK
    
    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = PURPLE
    
    def make_path(self):
        self.color = TURQUOISE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        pass

    def __lt__(self, other):
        return False
    
# Uses manhantan distance
# @p1 = point 1
# @p2 = point 2
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def make_grid(rows, width):
    grid = []
    GAP = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, GAP, rows)
            grid[i].append(node)
    
    return grid

def draw_grid(win, rows, width):
    GAP = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * GAP), (width, i * GAP))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * GAP, 0), (j * GAP, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()