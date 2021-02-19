import pygame
import random
import os

size = width, height = 800, 800
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


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
            all_sprites.remove(self.board[cell[1]][cell[0]])
            new_thing.hp = min(new_thing.hp + self.board[cell[1]][cell[0]].hpbuf, Character.MAX_HP)
            self.board[cell[1]][cell[0]] = new_thing
            self.board[coors[1]][coors[0]] = 0
            print(coors)
            return coors
        return None

    def get_click(self, mouse_pos, thing):
        cell = self.get_cell(mouse_pos)
        if cell:
            return self.on_click(cell, thing)
        return None


class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, cellx, celly, *group):
        self.image = image
        super().__init__(*group)
        self.cellx = cellx
        self.celly = celly
        self.rect = pygame.Rect(Board.X + cellx * Board.SIZE + 1,
                                Board.Y + celly * Board.SIZE + 1, Board.SIZE, Board.SIZE)
        self.rect.x = Board.X + cellx * Board.SIZE + 1
        self.rect.y = Board.Y + celly * Board.SIZE + 1


class Character(GameObject):
    MAX_HP = 100

    def __init__(self, image, cellx, celly, board, *group):
        super().__init__(image, cellx, celly, group)
        self.atk = 1
        self.hp = 10
        self.mana = 5
        self.gold = 0
        board.board[celly][cellx] = self
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


class Food(GameObject):
    def __init__(self, image, cellx, celly, buffs, board, *group):
        super().__init__(image, cellx, celly, group)
        self.manabuf = buffs['mana']
        self.attackbuf = buffs['attack']
        self.hpbuf = buffs['hp']
        board.board[celly][cellx] = self


def load_image(name, color_key=None):
    fullname = os.path.join('imgs', name)
    image = pygame.image.load(fullname).convert()

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


board = Board(5, 5)
image = load_image("character.png")
food_images = [load_image("croissant.png"), load_image("beet.png"),
               load_image("beer.png"), load_image("ginger.png")]
Player = Character(image, 1, 2, board, all_sprites)
board.set_view(Board.X, Board.Y, Board.SIZE)
running = True
for i in range(board.height):
    for j in range(board.width):
        if i == 1 and j == 2:
            continue
        BUFF = {'mana': 0, 'hp': random.randint(1, 10), 'attack': 0}
        Food(random.choice(food_images), i, j, BUFF, board, all_sprites)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            cell = board.get_cell(mouse_pos=pygame.mouse.get_pos())
            if cell:
                result = board.get_click(pygame.mouse.get_pos(), Player)
                if result:
                    BUFF = {'mana': 0, 'hp': random.randint(1, 10), 'attack': 0}
                    Food(random.choice(food_images), result[0], result[1], BUFF, board, all_sprites)
                print(Player.hp)
    screen.fill((0, 0, 0))
    board.render(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
