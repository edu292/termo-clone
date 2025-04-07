from sys import exit
from random import choice
from unidecode import unidecode
import pygame
import sys
import os


class PopUp:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.is_visible = False
        self.message = ''
        self.x = 0
        self.width = 0
        self.HEIGHT = 30
        self.y = 70
        self.SIDE_MARGIN = 10
        self.BACK_GROUND_COLOR = (0, 154, 254, 255)
        self.rect = pygame.Rect(self.x, self.y, screen_width, self.HEIGHT)
        self.FONT_SIZE = 20
        self.font = pygame.font.Font(resource_path('Mitr-Regular.ttf'), self.FONT_SIZE)

    def show(self, message):
        self.is_visible = True
        self.message = message
        self.width = self.font.size(self.message)[0]
        self.x = self.screen_width // 2 - self.width // 2
        self.rect = pygame.Rect(self.x - self.SIDE_MARGIN, self.y, self.width + self.SIDE_MARGIN * 2, self.HEIGHT)

    def draw(self):
        if not self.is_visible:
            return

        pygame.draw.rect(screen, self.BACK_GROUND_COLOR, self.rect)
        text_surface = self.font.render(self.message, True, FONT_COLOR)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.HEIGHT // 2))
        screen.blit(text_surface, text_rect)


class GameModeTAB:
    def __init__(self, screen_width):
        self.screen_width = screen_width
        self.game_modes = list(GAME_MODES.keys())
        self.game_mode = self.game_modes[0]
        self.tab_rects = []
        self.FONT_SIZE = 30
        self.font = pygame.font.Font(resource_path('Mitr-Regular.ttf'), self.FONT_SIZE)
        self.BACK_GROUND_COLOR = (34, 34, 34, 255)
        self.SELECTED_COLOR = (72,72,73,255)

        self.tab_height = 60
        self.spacing = 20

        last_width = 0
        for i, game_mode in enumerate(self.game_modes):
            width = self.font.size(game_mode)[0]
            rect = pygame.Rect(last_width+self.spacing, 0, width, self.tab_height)
            last_width += width + self.spacing
            self.tab_rects.append(rect)

    def draw(self):
        pygame.draw.rect(screen, self.BACK_GROUND_COLOR, (0, 0, self.screen_width, self.tab_height))
        for i, rect in enumerate(self.tab_rects):
            if self.game_mode == self.game_modes[i]:
                font_color = self.SELECTED_COLOR
            else:
                font_color = FONT_COLOR
            text_surface = self.font.render(self.game_modes[i], True, font_color)
            screen.blit(text_surface, rect)

    def clicked(self, pos):
        for i, rect in enumerate(self.tab_rects):
            if not rect.collidepoint(pos):
                continue
            self.game_mode = self.game_modes[i]
            return True


class Board:
    def __init__(self, x, rows=6, columns=5):
        self.rows = rows
        self.columns = columns
        self.CELL_SIZE = 50
        self.MARGIN = 10
        self.x = x
        self.y = 120
        self.cells = [[['letter empty', ''] for _ in range(self.columns)] for _ in range(self.rows)]
        self.rectangles = []
        self.current_row = 0
        self.create_rectangles()
        self.word = choice(word_bank)
        self.letters_in_word = {}
        self.letters_in_word = {letter: self.word.count(letter) for letter in self.word if
                           letter not in self.letters_in_word}
        print(self.word)
        self.done = False

    def check_guess(self):
        right_letters = 0
        wrong_place_letters = []
        letters_in_word = self.letters_in_word.copy()
        for index in range(self.columns):
            letter = self.cells[self.current_row][index][1]
            if self.word[index] == letter:
                right_letters += 1
                self.cells[self.current_row][index][0] = 'letter right'
                letters_in_word[letter] -= 1
            elif letter in self.word and letters_in_word[letter] > 0:
                wrong_place_letters.append((index, letter))
            else:
                self.cells[self.current_row][index][0] = 'letter wrong'
        for index, letter in wrong_place_letters:
            if letters_in_word[letter] > 0:
                self.cells[self.current_row][index][0] = 'letter right place'
                letters_in_word[letter] -= 1
            else:
                self.cells[self.current_row][index][0] = 'letter wrong'
        if right_letters == self.columns:
            self.done = True
        self.current_row += 1

    def place_letter(self, letter, index):
        self.cells[self.current_row][index][1] = letter

    def remove_letter(self, index):
        self.cells[self.current_row][index][1] = ''

    def create_rectangles(self):
        self.rectangles = []
        y = self.y + self.current_row * (self.CELL_SIZE + self.MARGIN)

        for index in range(len(self.cells[self.current_row])):
            x = self.x + index * (self.CELL_SIZE + self.MARGIN)
            self.rectangles.append(pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE))

    def draw(self, current_letter_index):
        STATE_COLORS = {
            'letter empty': (97, 84, 88, 255),  # gray
            'letter right': (58, 163, 148, 255),  # green
            'letter right place': (211, 173, 105, 255),  # yellow
            'letter wrong': (49, 42, 44, 255),
            'letter current line': (76, 67, 71, 255)
        }

        for row_idx, row in enumerate(self.cells):
            for col_idx, (state, char) in enumerate(row):
                x = self.x + col_idx * (self.CELL_SIZE + self.MARGIN)
                y = self.y + row_idx * (self.CELL_SIZE + self.MARGIN)
                if row_idx == self.current_row and not self.done:
                    state = 'letter current line'

                pygame.draw.rect(screen, STATE_COLORS[state], (x, y, self.CELL_SIZE, self.CELL_SIZE))

                if state == 'letter current line':
                    pygame.draw.rect(screen, BACKGROUND_COLOR,(x + 3, y + 3, self.CELL_SIZE -6, self.CELL_SIZE - 6))
                    if col_idx == current_letter_index:
                        pygame.draw.rect(screen, STATE_COLORS[state], (x, y+self.CELL_SIZE-6, self.CELL_SIZE, 6))

                if char:
                    text_surface = BOARD_FONT.render(char.upper(), True, FONT_COLOR)
                    text_rect = text_surface.get_rect(center=(x + self.CELL_SIZE // 2, y + self.CELL_SIZE // 2))
                    screen.blit(text_surface, text_rect)


class Game:
    def __init__(self, game_mode):
        self.GAME_MODES = GAME_MODES
        self.game_mode = game_mode
        self.boards = self.create_boards()
        self.words = [board.word for board in self.boards]
        self.uncompleted_boards = self.boards.copy()
        self.guess = ['' for _ in range(5)]
        self.current_letter_index = 0
        self.current_row = 0
        self.rows = self.GAME_MODES[self.game_mode][1]
        self.clicked = False

    def check_won(self):
        if not self.uncompleted_boards:
            if self.current_row < self.rows:
                popup.show(choice(WON_MESSAGES))
            elif self.current_row == self.rows:
                popup.show(choice(WON_LAST_LINE_MESSAGES))
        elif self.current_row == self.rows:
            message = 'Palavras: '
            for index, word in enumerate(self.words):
                message += word
                if index < len(self.words) - 1:
                    message += ', '
            popup.show(message)
        else:
            for board in self.uncompleted_boards:
                board.create_rectangles()


    def create_boards(self):
        pygame.display.set_caption(self.game_mode.capitalize())
        if self.game_mode == "termo":
            return [Board(50)]
        elif self.game_mode == "dueto":
            return [Board(50, rows=7), Board(400, rows=7)]
        elif self.game_mode == "quarteto":
            return [Board(50, rows=9), Board(400, rows=9), Board(750, rows=9), Board(1100, rows=9)]

    def back_space(self):
        if self.current_letter_index > 0 and not self.clicked:
            self.current_letter_index -= 1
        for board in self.uncompleted_boards:
            board.remove_letter(self.current_letter_index)
            self.guess[self.current_letter_index] = ''
        self.clicked = False

    def check_guess(self):
        guess_str = ''.join(self.guess)
        if len(guess_str) != 5:
            return
        if guess_str not in word_bank:
            popup.show('essa palavra não é aceita')
            return
        self.guess = ['' for _ in range(5)]
        self.current_letter_index = 0
        done_board = None
        for board in self.uncompleted_boards:
            board.check_guess()
            if board.done:
                done_board = board
        if done_board:
            self.uncompleted_boards.remove(done_board)
        self.current_row += 1
        self.check_won()

    def skip_letter(self):
        if self.current_letter_index < 4:
            self.current_letter_index += 1
            self.clicked = True

    def previous_letter(self):
        if self.current_letter_index > 0:
            self.current_letter_index -= 1
            self.clicked = True

    def place_letter(self, letter):
        if self.current_letter_index > 4:
            return
        if not self.uncompleted_boards:
            return
        for board in self.uncompleted_boards:
            board.place_letter(letter, self.current_letter_index)
            self.guess[self.current_letter_index] = letter
        self.current_letter_index += 1
        self.clicked = False

    def click(self, pos):
        for board in self.uncompleted_boards:
            for rectangle in board.rectangles:
                if rectangle.collidepoint(pos):
                    self.current_letter_index = board.rectangles.index(rectangle)
                    self.clicked = True

    def draw(self):
        for board in self.boards:
            board.draw(self.current_letter_index)


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 700
BACKGROUND_COLOR = (110, 92, 98, 255)
FONT_COLOR = (250, 250, 255, 255)
GAME_MODES = {'termo': (1, 6),
              'dueto': (2, 7),
              'quarteto': (4, 9)}
WON_MESSAGES = ['Fenomenal', 'Impressionante', 'Extraordinário']
WON_LAST_LINE_MESSAGES = ['Ufa!']

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
icon = pygame.image.load(resource_path('icon.png'))
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
BOARD_FONT = pygame.font.Font(resource_path('Mitr-Bold.ttf'), 40)

with open('palavras.txt', 'r') as arquivo:
    word_bank = arquivo.read().splitlines()
    word_bank = [word for word in word_bank if len(word) == 5]

game = Game("termo")
game_mode_ui = GameModeTAB(SCREEN_WIDTH)
popup = PopUp(SCREEN_WIDTH)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.KEYDOWN:
            popup.is_visible = False
            if event.key == pygame.K_BACKSPACE:
                game.back_space()
            elif event.key == pygame.K_RETURN:
                game.check_guess()
            elif event.key == pygame.K_SPACE or event.key == pygame.K_RIGHT:
                game.skip_letter()
            elif event.key == pygame.K_LEFT:
                game.previous_letter()
            else:
                letter = unidecode(event.unicode)
                if not letter.isalpha():
                    continue
                game.place_letter(letter)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            popup.is_visible = False
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if game_mode_ui.clicked(pos):
                    game = Game(game_mode_ui.game_mode)
                    continue
                game.click(pos)

    screen.fill(BACKGROUND_COLOR)
    game_mode_ui.draw()
    game.draw()
    popup.draw()

    pygame.display.update()
    clock.tick(60)
