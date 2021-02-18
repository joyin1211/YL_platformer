import pygame

size = width, height = 800, 400
screen = pygame.display.set_mode(size)


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for x in range(self.width):
            for y in range(self.height):
                if self.board[y][x] == 1:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (self.left + x * self.cell_size,
                                      self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(screen, (255, 255, 255),
                                     (self.left + x * self.cell_size,
                                      self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        x, y = int((mouse_pos[0] - self.left) / self.cell_size),\
               int((mouse_pos[1] - self.top) / self.cell_size)
        return x, y

    def on_click(self, cell):
        if self.board[cell[1]][cell[0]] == 0:
            self.board[cell[1]][cell[0]] = 1
        else:
            self.board[cell[1]][cell[0]] = 0

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if 0 <= cell[0] < self.width and 0 <= cell[1] < self.height:
            self.on_click(cell)


board = Board(4, 3)
board.set_view(100, 100, 50)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.get_click(event.pos)
    screen.fill((0, 0, 0))
    board.render(screen)
    pygame.display.flip()
