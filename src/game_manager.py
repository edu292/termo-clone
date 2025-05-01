from src.ui.popup import PopUp
from src.ui.gamemode_tab import GameModeTAB
from src.models.game import Game
import pygame
from unidecode import unidecode


class GameManager:
    def __init__(self, renderer):
        self.renderer = renderer
        self.game_mode_tab = GameModeTAB(renderer)
        self.pop_up = PopUp(renderer)
        self.game = Game(renderer, 'termo', self.pop_up)


    def handle_click(self, pos):
        self.pop_up.erase()
        if self.game_mode_tab.clicked(pos):
            self.game = Game(self.renderer, self.game_mode_tab.game_mode, self.pop_up)
            self.renderer.clear_screen()
            return
        self.game.click(pos)

    def handle_key(self, key, letter):
        self.pop_up.erase()
        if key == pygame.K_BACKSPACE:
            self.game.back_space()
        elif key == pygame.K_RETURN:
            self.game.check_guess()
        elif key == pygame.K_SPACE or key == pygame.K_RIGHT:
            self.game.skip_letter()
        elif key == pygame.K_LEFT:
            self.game.previous_letter()
        else:
            if not letter.isalpha():
                return
            self.game.place_letter(unidecode(letter))

    def draw(self):
        self.game.draw()
        self.game_mode_tab.draw()
        self.pop_up.draw()