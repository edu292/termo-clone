from src.game_manager import GameManager
from src.renderer import Renderer
from src.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.utils.helpers import resource_path
import pygame

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load(resource_path('assets/icon/icon.png'))
pygame.display.set_icon(icon)

clock = pygame.Clock()
renderer = Renderer(screen)
game_manager = GameManager(renderer)

renderer.clear_screen()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            game_manager.handle_key(event.key, event.unicode)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            game_manager.handle_click(pos)
    game_manager.draw()
    pygame.display.update()
    clock.tick(60)
pygame.quit()
