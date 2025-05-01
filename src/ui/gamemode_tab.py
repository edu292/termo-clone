from src.config import FONT_COLOR, GAME_MODES, SCREEN_WIDTH, Fonts


class GameModeTAB:
    def __init__(self, renderer):
        self.renderer = renderer
        self.game_modes = list(GAME_MODES.keys())
        self.game_mode = self.game_modes[0]
        self.FONT_SIZE = 30
        self.BACK_GROUND_COLOR = (34, 34, 34, 255)
        self.SELECTED_COLOR = (72,72,73,255)
        self.tab_height = 60
        self.spacing = 20
        self.tab_rects = self.create_game_mode_rects()

    def create_game_mode_rects(self):
        last_width = 0
        tab_rects = []
        for i, game_mode in enumerate(self.game_modes):
            width = self.renderer.get_text_size(game_mode, Fonts.TAB)[0]
            rect = self.renderer.get_rect(last_width + self.spacing, 0, width, self.tab_height)
            last_width += width + self.spacing
            tab_rects.append(rect)

        return tab_rects

    def draw(self):
        self.renderer.draw_rect(self.BACK_GROUND_COLOR, (0, 0, SCREEN_WIDTH, self.tab_height))
        for i, rect in enumerate(self.tab_rects):
            if self.game_mode == self.game_modes[i]:
                font_color = self.SELECTED_COLOR
            else:
                font_color = FONT_COLOR
            self.renderer.draw_text(self.game_modes[i],
                                    Fonts.TAB,
                                    font_color,
                                    rect.center,
                                    center=True)

    def clicked(self, pos):
        for i, rect in enumerate(self.tab_rects):
            if not rect.collidepoint(pos):
                continue
            self.game_mode = self.game_modes[i]
            self.draw()
            return True
        return False