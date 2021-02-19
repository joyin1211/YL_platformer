import pygame


class Board:
    # создание поля
    SIZE = 100
    X = 150
    Y = 150

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
                '''
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
                '''
                pygame.draw.rect(screen, (255, 255, 255),
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)
                pass

    def get_cell(self, mouse_pos):
        if self.left <= mouse_pos[0] <= self.left + self.cell_size * self.width and \
                self.top <= mouse_pos[1] <= self.top + self.cell_size * self.height:
            x, y = int((mouse_pos[0] - self.left) / self.cell_size), \
                   int((mouse_pos[1] - self.top) / self.cell_size)
            return x, y
        return None

    def on_click(self, cell, new_thing):
        coors = new_thing.cellx, new_thing.celly
        if new_thing.move(cell[0], cell[1]):
            self.board[cell[1]][cell[0]] = new_thing
            print(cell[0], cell[1])
            self.board[coors[1]][coors[0]] = 0
            print(self.board)

    def get_click(self, mouse_pos, thing):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell, thing)
        return cell


class Character(pygame.sprite.Sprite):
    def __init__(self, image, cellx, celly, *group):
        self.image = image
        super().__init__(*group)
        self.cellx = cellx
        self.celly = celly
        self.rect = pygame.Rect(Board.X + cellx * Board.SIZE,
                                Board.Y + celly * Board.SIZE, Board.SIZE, Board.SIZE)
        self.rect.x = Board.X + cellx * Board.SIZE
        self.rect.y = Board.Y + celly * Board.SIZE
        self.atk = 1
        self.hp = 10
        self.mana = 5
        pass

    def move(self, coor1, coor2):
        if coor2 == self.celly and abs(coor1 - self.cellx) == 1:
            self.cellx = coor1
            self.rect.x = Board.X + self.cellx * Board.SIZE
            self.rect.y = Board.Y + self.celly * Board.SIZE
            return True
        elif coor1 == self.cellx and abs(coor2 - self.celly) == 1:
            self.celly = coor2
            self.rect.x = Board.X + self.cellx * Board.SIZE
            self.rect.y = Board.Y + self.celly * Board.SIZE
            return True
        return False


class Item(pygame.sprite.Sprite):
    def __init__(self, image, cellx, celly, *group):
        self.image = image
        super().__init__(*group)
        self.cellx = cellx
        self.celly = celly
        self.rect = pygame.Rect(Board.X + cellx * Board.SIZE,
                                Board.Y + celly * Board.SIZE, Board.SIZE, Board.SIZE)
        self.rect.x = Board.X + cellx * Board.SIZE
        self.rect.y = Board.Y + celly * Board.SIZE
