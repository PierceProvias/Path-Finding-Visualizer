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

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED
    
    def make_open(self):
        self.color = GREEN
    
    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = ORANGE
    
    def make_end(self):
        self.color = PURPLE
    
    def make_path(self):
        self.color = TURQUOISE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        # If not barriers add into neighbors list
        self.neighbors = []
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        
        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
        

    def __lt__(self, other):
        return False
    
# Uses manhantan distance
# @p1 = point 1
# @p2 = point 2
def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}      # Previous node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]     # Popping lowest value f_score
        open_set_hash.remove(current)    
        if current == end:      # found shortest path
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True    
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()
    return False

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

def get_clicked_pos(pos, rows, width):
    GAP = width // rows
    y, x = pos
    row = y // GAP
    col = x // GAP
    return row, col

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, WIDTH)

    start_pos = None
    end_pos = None

    run = True
    started = False
    while run:
        draw(WIN, grid, ROWS, WIDTH)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 run = False
            
            if started:
                continue
            if pygame.mouse.get_pressed()[0]:   # Left mouse button
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                
                if not start_pos and node != end_pos:
                    start_pos = node
                    start_pos.make_start()

                elif not end_pos and node != start_pos:
                    end_pos = node
                    end_pos.make_end()

                elif node != end_pos and node != start_pos:
                    node.make_barrier()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pos = pygame.mouse.get_pos()
                    row, col = get_clicked_pos(pos, ROWS, WIDTH)
                    node = grid[row][col]
                    node.reset()
                    if node == start_pos:
                        start_pos = None
                    elif node == end_pos:
                        end_pos = None
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algorithm(lambda: draw(win, grid, ROWS, WIDTH), grid, start_pos, end_pos)
    pygame.quit()

main(WIN, WIDTH)