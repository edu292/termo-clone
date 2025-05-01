from src.config import BACKGROUND_COLOR, FONT_COLOR, SCREEN_WIDTH, Fonts

class PopUp:
    def __init__(self, renderer):
        self.renderer = renderer
        self.to_draw = False
        self.is_visible = False
        self.message = ''
        self.x = 0
        self.width = 0
        self.HEIGHT = 30
        self.y = 70
        self.SIDE_MARGIN = 10
        self.BACKGROUND_COLOR = (0, 154, 254, 255)
        self.rect = self.renderer.get_rect(self.x, self.y, SCREEN_WIDTH, self.HEIGHT)

    def show(self, message):
        self.to_draw = True
        self.message = message
        self.width = self.renderer.get_text_size(self.message, Fonts.POPUP)[0]
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.rect = self.renderer.get_rect(self.x - self.SIDE_MARGIN, self.y, self.width + self.SIDE_MARGIN * 2,
                                           self.HEIGHT)

    def erase(self):
        if not self.is_visible:
            return
        self.renderer.draw_rect(BACKGROUND_COLOR, self.rect)

    def draw(self):
        if not self.to_draw:
            return

        self.renderer.draw_rect(self.BACKGROUND_COLOR, self.rect)
        self.renderer.draw_text(self.message,
                                Fonts.POPUP,
                                FONT_COLOR,
                                (self.x + self.width // 2, self.y + self.HEIGHT // 2),
                                center=True)
        self.to_draw = False
        self.is_visible = True