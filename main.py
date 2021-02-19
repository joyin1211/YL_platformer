import pygame
import random
import os

from Game import Game

size = width, height = 800, 800
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()
IS_GAME_OVER = False
IS_GAME_STARTED = False
g = Game()
pygame.font.init()
while g.running:
    g.curr_menu.display_menu()
    g.game_loop()


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
        global IS_GAME_OVER
        coors = new_thing.cellx, new_thing.celly
        if new_thing.move(cell[0], cell[1]):
            if type(self.board[cell[1]][cell[0]]) != Enemy:
                all_sprites.remove(self.board[cell[1]][cell[0]])
                new_thing.hp = min(new_thing.hp + self.board[cell[1]][cell[0]].hpbuf, Character.MAX_HP)
                new_thing.atk = new_thing.hp + self.board[cell[1]][cell[0]].attackbuf
                self.board[cell[1]][cell[0]] = new_thing
                self.board[coors[1]][coors[0]] = 0
                return coors
            else:
                if new_thing.atk >= self.board[cell[1]][cell[0]].hp:
                    new_thing.gold += self.board[cell[1]][cell[0]].gold
                    new_thing.hp -= self.board[cell[1]][cell[0]].atk
                    if new_thing.hp <= 0:
                        IS_GAME_OVER = True
                    all_sprites.remove(self.board[cell[1]][cell[0]])
                    self.board[cell[1]][cell[0]] = new_thing
                    self.board[coors[1]][coors[0]] = 0
                    return coors
                else:
                    new_thing.hp -= self.board[cell[1]][cell[0]].atk
                    if new_thing.hp <= 0:
                        IS_GAME_OVER = True
                    new_thing.move(coors[0], coors[1])
                    return None
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
        self.attackbuf = buffs['attack']
        self.hpbuf = buffs['hp']
        board.board[celly][cellx] = self


class Weapon(GameObject):
    def __init__(self, image, cellx, celly, buffs, board, *group):
        super().__init__(image, cellx, celly, group)
        self.attackbuf = buffs['attack']
        self.hpbuf = buffs['hp']
        board.board[celly][cellx] = self


class Enemy(GameObject):
    def __init__(self, image, cellx, celly, atk, hp, gold, board, *group):
        super().__init__(image, cellx, celly, group)
        self.atk = atk
        self.hp = hp
        self.gold = gold
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
weapon_images = [load_image("katana.png"), load_image("bone-knife.png")]
enemy_stats = [(load_image("gorilla.png"), 3, 1, 7),
               (load_image("mantis.png"), 2, 5, 7)]
Player = Character(image, 1, 2, board, all_sprites)
board.set_view(Board.X, Board.Y, Board.SIZE)
myfont = pygame.font.SysFont('Comic Sans MS', 30)
running = True
for i in range(board.height):
    for j in range(board.width):
        if i == 1 and j == 2:
            continue
        choose_type = random.randint(1, 3)
        if choose_type == 1:
            BUFF = {'hp': random.randint(1, 5), 'attack': 0}
            Food(random.choice(food_images), i, j, BUFF, board, all_sprites)
        elif choose_type == 2:
            result = random.choice(enemy_stats)
            Enemy(result[0], i, j, result[1], result[2], result[3], board, all_sprites)
        else:
            BUFF = {'hp': 0, 'attack': random.randint(1, 5)}
            Food(random.choice(weapon_images), i, j, BUFF, board, all_sprites)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            cell = board.get_cell(mouse_pos=pygame.mouse.get_pos())
            if cell:
                result = board.get_click(pygame.mouse.get_pos(), Player)
                if result:
                    choose_type = random.randint(1, 3)
                    if choose_type == 1:
                        BUFF = {'hp': random.randint(1, 5), 'attack': 0}
                        Food(random.choice(food_images), result[0], result[1], BUFF, board, all_sprites)
                    elif choose_type == 2:
                        reslt = random.choice(enemy_stats)
                        Enemy(reslt[0], result[0], result[1], reslt[1], reslt[2], reslt[3], board, all_sprites)
                    else:
                        BUFF = {'hp': 0, 'attack': random.randint(1, 5)}
                        Food(random.choice(weapon_images), result[0], result[1], BUFF, board, all_sprites)
    screen.fill((0, 0, 0))
    if IS_GAME_OVER:
        exit(0)
    else:
        board.render(screen)
        all_sprites.draw(screen)
        textsurface = myfont.render("HP: {}".format(str(Player.hp)), False, (255, 255, 255))
        textsurface1 = myfont.render("ATK: {}".format(str(Player.atk)), False, (255, 255, 255))
        textsurface2 = myfont.render("GOLD: {}".format(str(Player.gold)), False, (255, 255, 255))
        screen.blit(textsurface, (0, 0))
        screen.blit(textsurface1, (0, 30))
        screen.blit(textsurface2, (0, 60))
        pygame.display.flip()
