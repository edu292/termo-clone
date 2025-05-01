from src.config import GAME_MODES, WON_MESSAGES, WON_LAST_LINE_MESSAGES, word_bank
from src.models.board import Board
from random import choice

class Game:
    def __init__(self, renderer, game_mode, pop_up):
        self.renderer = renderer
        self.GAME_MODES = GAME_MODES
        self.game_mode = game_mode
        self.pop_up = pop_up
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
                self.pop_up.show(choice(WON_MESSAGES))
            elif self.current_row == self.rows:
                self.pop_up.show(choice(WON_LAST_LINE_MESSAGES))
        elif self.current_row == self.rows:
            message = 'Palavras: '
            for index, word in enumerate(self.words):
                message += word
                if index < len(self.words) - 1:
                    message += ', '
            self.pop_up.show(message)
        else:
            for board in self.uncompleted_boards:
                board.create_rectangles()

    def create_boards(self):
        self.renderer.set_caption(self.game_mode.capitalize())
        if self.game_mode == "termo":
            return [Board(self.renderer, 50)]
        elif self.game_mode == "dueto":
            return [Board(self.renderer, 50, rows=7), Board(self.renderer, 400, rows=7)]
        elif self.game_mode == "quarteto":
            return [Board(self.renderer, 50, rows=9), Board(self.renderer, 400, rows=9), Board(self.renderer, 750, rows=9), Board(self.renderer, 1100, rows=9)]

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
            self.pop_up.show('essa palavra não é aceita')
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
