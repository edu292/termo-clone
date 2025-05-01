import pygame
import pygame.constants
from src.utils.helpers import resource_path
from src.config import FONT_COLOR, BACKGROUND_COLOR, Fonts


class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.fonts = {}
        self.clock = pygame.time.Clock()
        self.init_fonts()

    def init_fonts(self):
        self.fonts = {
            Fonts.BOARD: pygame.font.Font(resource_path('assets/fonts/Mitr-Bold.ttf'), 40),
            Fonts.TAB: pygame.font.Font(resource_path('assets/fonts/Mitr-Regular.ttf'), 30),
            Fonts.POPUP: pygame.font.Font(resource_path('assets/fonts/Mitr-Regular.ttf'), 20)
        }

    def clear_screen(self):
        self.screen.fill(BACKGROUND_COLOR)

    def draw_rect(self, color, rect):
        pygame.draw.rect(self.screen, color, rect)

    @staticmethod
    def get_rect(x, y, width, height):
        return pygame.Rect((x, y, width, height))

    def draw_text(self, text, font, color, position, center=False):
        font = self.fonts[font]
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=position)
        else:
            text_rect = text_surface.get_rect(topleft=position)
        self.screen.blit(text_surface, text_rect)
        return text_rect

    def get_text_size(self, text, font):
        font = self.fonts[font]
        return font.size(text)

    @staticmethod
    def set_caption(caption):
        pygame.display.set_caption(caption)

