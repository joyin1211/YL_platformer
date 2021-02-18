import pygame
from structs import Board, Character
import os

size = width, height = 800, 800
screen = pygame.display.set_mode(size)
all_sprites = pygame.sprite.Group()


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
Player = Character(image, 2, 2, all_sprites)
board.set_view(Board.X, Board.Y, Board.SIZE)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            cell = board.get_click(event.pos, Player)
            if cell:
                Player.move(cell[0], cell[1])
    screen.fill((0, 0, 0))
    board.render(screen)
    all_sprites.draw(screen)
    pygame.display.flip()
