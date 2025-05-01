from enum import Enum, auto
from src.utils.helpers import load_word_bank

class CellStates(Enum):
    EMPTY = auto()
    WRONG = auto()
    WRONG_PLACE = auto()
    RIGHT = auto()
    CURRENT_LINE = auto()


class Fonts(Enum):
    BOARD = auto()
    TAB = auto()
    POPUP = auto()


STATE_COLORS = {CellStates.EMPTY: (97, 84, 88, 255),
                CellStates.RIGHT: (58, 163, 148, 255),
                CellStates.WRONG_PLACE: (211, 173, 105, 255),
                CellStates.WRONG: (49, 42, 44, 255),
                CellStates.CURRENT_LINE: (76, 67, 71, 255)}

SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (110, 92, 98, 255)
FONT_COLOR = (250, 250, 255, 255)
GAME_MODES = {'termo': (1, 6),
              'dueto': (2, 7),
              'quarteto': (4, 9)}
WON_MESSAGES = ['Fenomenal', 'Impressionante', 'Extraordinário']
WON_LAST_LINE_MESSAGES = ['Ufa!']
word_bank = load_word_bank('assets/words/words.txt')